#include "OpenAL.h"

#include "AL/al.h"
#include "AL/alc.h"
#include "AL/alext.h"

#include "vorbis/vorbisfile.h"
#include <string>

static ALenum soundErr;

#define AL_CHECK(...) \
{ \
	if ((soundErr = alGetError()) != AL_NO_ERROR) { \
		LOG("OpenAL error: %x at %s(%i)", soundErr, __FILE__, __LINE__); \
		check_error(); \
		return ERROR; \
	} \
}

#define EXCEPTION(...) \
{ \
	LOG_ERROR(__VA_ARGS__); \
	return ERROR; \
}

OpenAL::OpenAL()
	:initialized(false)
{

}
OpenAL::~OpenAL()
{

}

bool OpenAL::initAL()
{
	const ALCchar* name;
	ALCdevice* device;
	ALCcontext* ctx;

	/* Open and initialize a device */
	device = alcOpenDevice(NULL);
	if (!device)
	{
		LOG("Could not open a device!");
		return false;
	}

	ctx = alcCreateContext(device, NULL);
	if (ctx == NULL || alcMakeContextCurrent(ctx) == ALC_FALSE)
	{
		if (ctx != NULL)
			alcDestroyContext(ctx);
		alcCloseDevice(device);
		LOG("Could not set a context!\n");
		return false;
	}

	name = NULL;
	if (alcIsExtensionPresent(device, "ALC_ENUMERATE_ALL_EXT"))
		name = alcGetString(device, ALC_ALL_DEVICES_SPECIFIER);
	if (!name || alcGetError(device) != AL_NO_ERROR)
		name = alcGetString(device, ALC_DEVICE_SPECIFIER);
	LOG("Opened \"%s\"\n", name);

	initialized = true;
	return true;
}

/* closeAL closes the device belonging to the current context, and destroys the
* context. */
void OpenAL::closeAL(void)
{
	ALCdevice* device;
	ALCcontext* ctx;

	ctx = alcGetCurrentContext();
	if (ctx == NULL)
		return;

	device = alcGetContextsDevice(ctx);

	alcMakeContextCurrent(NULL);
	alcDestroyContext(ctx);
	alcCloseDevice(device);
}

int OpenAL::addBufferWav(char* fnameptr) {
	LOG("addBuffer( %s )", fnameptr);

	BasicWAVEHeader header;

	char* data = readWav(fnameptr, &header);
	if (data) {
		//Now We've Got A Wave In Memory, Time To Turn It Into A Usable Buffer
		ALuint buffer = createBufferFromWave(data, header);
		if (buffer) {
			return (int)buffer;

		}
		else LOG("Failed to create buffer");
		free(data);

	}
	else LOG("Failed to read file");

	return ERROR;
}

int OpenAL::addBufferOgg(char* fnameptr)
{
	ALenum error = 0;
	ALuint sound = 0;
	FILE* fp = 0;
	OggVorbis_File vf;
	vorbis_info* vi = 0;
	ALenum format = 0;
	char* pcmout = 0;

	// open the file in read binary mode
	fp = fopen(fnameptr, "rb");
	if (fp == 0) {
		LOG("Could not open file `%s`\n", fnameptr);
		return ERROR;
	}

	// make a buffer
	alGenBuffers(1, &sound);

	// check for errors
	if ((error = alGetError()) != AL_NO_ERROR) {
		LOG("Failed to generate sound buffer %d\n", error);
		return ERROR;
	}
	
	// open the ogg vorbis file. This is a must on windows, do not use ov_open.
	// set OV_CALLBACKS_NOCLOSE else it will close your fp when ov_close() is reached, which is fine.
	if (ov_open_callbacks(fp, &vf, NULL, 0, OV_CALLBACKS_NOCLOSE) < 0) {
		LOG("Stream is not a valid OggVorbis stream!\n");
		return ERROR;
	}


	// fill vi with a new ogg vorbis info struct, determine audio format
	// audio format will always been a length of 16bits, vi->channels determines mono or stereo
	vi = ov_info(&vf, -1);
	format = vi->channels == 1 ? AL_FORMAT_MONO16 : AL_FORMAT_STEREO16;

	// data_len is the amount of data to read, allocate said data space
	// this is calculated by (samples * channels * 2 (aka 16bits))
	size_t data_len = ov_pcm_total(&vf, -1) * vi->channels * 2;
	pcmout = (char*)malloc(data_len);
	if (pcmout == 0) {
		LOG("Out of memory.\n");
		return ERROR;
	}

	// fill pcmout buffer with ov_read data samples
	// you can't just slap data_len in place of 4096, it doesn't work that way
	// 0 is endianess, 0 for little, 1 for big
	// 2 is the data type short's size, mine is 2
	// 1 is the signedness you want, I want short not unsigned short (for openal) so 1
	for (size_t size = 0, offset = 0, sel = 0;
		(size = ov_read(&vf, (char*)pcmout + offset, 4096, 0, 2, 1, (int*)&sel)) != 0;
		offset += size) {
		if (size < 0)
			puts("Faulty ogg file :o"); // use https://xiph.org/vorbis/doc/vorbisfile/ov_read.html for handling enums
	}

	// send data to openal, vi->rate is your freq in Hz, dont assume 44100
	alBufferData(sound, format, pcmout, data_len, vi->rate);
	if ((error = alGetError()) != AL_NO_ERROR) {
		LOG("Failed to send audio information buffer to OpenAL! 0x%06x\n", error);
		return ERROR;
	}

	// free your resources >:(
	free(pcmout);
	fclose(fp);
	ov_clear(&vf);
	return sound;
}

int OpenAL::releaseBuffer(int bufferId) {
	LOG("releaseBuffer( %i )", bufferId);
	ALuint buffer = bufferId;
	alDeleteBuffers(1, &buffer);

	AL_CHECK();
	return SUCCESS;
}

// Source Handling
// -----------------------------------

int OpenAL::addSource(int bufferId) {

	ALuint src = 0;
	alGenSources(1, &src);

	LOG("addSource( %i ) -> id %i", bufferId, src);
	AL_CHECK();

	alSourcei(src, AL_BUFFER, bufferId);
	alSourcef(src, AL_ROLLOFF_FACTOR, 0.25);

	AL_CHECK();
	return src;
}

int OpenAL::releaseSource(int sourceId) {
	LOG("releaseSource( %i )", sourceId);

	ALuint source = sourceId;
	alDeleteSources(1, &source);

	AL_CHECK();
	return SUCCESS;
}

int OpenAL::setPositon(int sourceId, float x, float y, float z) {
	if (isInitialized()) {
		// LOG_VERBOSE("setPositon( %i, %.2f, %.2f, %.2f )", sourceId, x, y, z);
		float pos[] = { x, y, z };
		alSourcefv(sourceId, AL_POSITION, pos);

		AL_CHECK();
	}
	return SUCCESS;
}

int OpenAL::setPitch(int sourceId, float pitch) {
	if (isInitialized()) {
		LOG("setPitch( %i, %.2f )", sourceId, pitch);
		alSourcef(sourceId, AL_PITCH, pitch);

		AL_CHECK();
	}
	return SUCCESS;
}

int OpenAL::setGain(int sourceId, float gain) {
	if (isInitialized()) {
		LOG("setGain( %i, %.2f )", sourceId, gain);
		alSourcef(sourceId, AL_GAIN, gain);

		AL_CHECK();
	}
	return SUCCESS;
}

int OpenAL::setRolloff(int sourceId, float rolloff) {
	if (isInitialized()) {
		LOG("setRolloff( %i, %.2f )", sourceId, rolloff);
		alSourcef(sourceId, AL_ROLLOFF_FACTOR, rolloff);

		AL_CHECK();
	}
	return SUCCESS;
}

int OpenAL::play(int sourceId, int loop) {
	if (isInitialized()) {
		LOG("play( %i, %i )", sourceId, loop);
		alSourcei(sourceId, AL_LOOPING, loop);
		alSourcePlay(sourceId);

		AL_CHECK();
	}
	return SUCCESS;
}

int OpenAL::stop(int sourceId) {
	if (isInitialized()) {
		LOG("stop( %i )", sourceId);
		alSourceStop(sourceId);

		AL_CHECK();
	}
	return SUCCESS;
}


// Listener Handling
// -----------------------------------

int OpenAL::setListenerPosition(float x, float y, float z) {
	if (isInitialized()) {
		// LOG_VERBOSE("setListenerPosition( %.2f, %.2f, %.2f )", x, y, z);
		float listenerPos[] = { x, y, z };
		alListenerfv(AL_POSITION, listenerPos);

		AL_CHECK();
	}
	return SUCCESS;
}


int OpenAL::setListenerOrientation(float xAt, float yAt, float zAt, float xUp, float yUp, float zUp) {
	if (isInitialized()) {
		// LOG_VERBOSE("setListenerOrientation( %.2f, %.2f, %.2f, %.2f, %.2f, %.2f  )", xAt, yAt, zAt, xUp, yUp, zUp);
		float listenerOri[] = { xAt, yAt, zAt, xUp, yUp, zUp };
		alListenerfv(AL_ORIENTATION, listenerOri);

		AL_CHECK();
	}
	return SUCCESS;
}



// Initialization & Release
// -----------------------------------

//WARNING: This Doesn't Check To See If These Pointers Are Valid
// This method is from http://www.gamedev.net/community/forums/topic.asp?topic_id=505152&whichpage=1&#3296091
char* OpenAL::readWav(char* filename, BasicWAVEHeader* header) {

	FILE* file = fopen(filename, "rb");
	if (!file) {
		LOG_WARN("readWAVE() - fopen failed");
		return 0;
	}

	if (fread(header, sizeof(BasicWAVEHeader), 1, file)) {
		if (!(//these things *must* be valid with this basic header
			memcmp("RIFF", header->riff, 4) ||
			memcmp("WAVE", header->wave, 4) ||
			memcmp("fmt ", header->fmt, 4) ||
			memcmp("data", header->data, 4)
			)) {
			char* buffer = (char*)malloc(header->dataSize);
			if (buffer) {
				if (fread(buffer, header->dataSize, 1, file)) {
					fclose(file);
					return buffer;
				}
				else {
					LOG_WARN("readWAVE() - fread (inner) failed");
				}
				free(buffer);
			}
			else {
				LOG_WARN("readWAVE() - buffer not allocated");
			}
		}
		else {
			LOG_WARN("readWAVE() - header not valid");
		}
	}
	else {
		LOG_WARN("readWAVE() - fread failed");
	}
	fclose(file);
	return 0;
}

// This method is from http://www.gamedev.net/community/forums/topic.asp?topic_id=505152&whichpage=1&#3296091
ALuint OpenAL::createBufferFromWave(char* data, BasicWAVEHeader header) {

	ALuint buffer = 0;

	ALuint format = 0;
	switch (header.bitsPerSample) {
	case 8:
		format = (header.channels == 1) ? AL_FORMAT_MONO8 : AL_FORMAT_STEREO8;
		break;
	case 16:
		format = (header.channels == 1) ? AL_FORMAT_MONO16 : AL_FORMAT_STEREO16;
		break;
	default:
		LOG("readWAVE() - unsupported bitrate %i", header.bitsPerSample);
		return 0;
	}

	alGenBuffers(1, &buffer);
	alBufferData(buffer, format, data, header.dataSize, header.samplesPerSec);
	return buffer;
}

int OpenAL::check_error() {
	ALenum error = alGetError();

	if (error == AL_NO_ERROR)
		return SUCCESS;

	if (error == AL_INVALID_NAME)
		LOG("AL_INVALID_NAME, error code %i", error);

	if (error == AL_INVALID_ENUM)
		LOG("AL_INVALID_ENUM, error code %i", error);

	if (error == AL_INVALID_VALUE)
		LOG("AL_INVALID_VALUE, error code %i", error);

	if (error == AL_INVALID_OPERATION)
		LOG("AL_INVALID_OPERATION, error code %i", error);

	if (error == AL_OUT_OF_MEMORY)
		LOG("AL_OUT_OF_MEMORY, error code %i", error);

	return ERROR;
}

/* LoadBuffer loads the named audio file into an OpenAL buffer object, and
	* returns the new buffer ID.
	*/
ALuint OpenAL::loadSound(char* filename)
{
	std::string fn = filename;

	std::string extension = fn.substr(fn.length() - 3, 3);
	char* sub = filename + strlen(filename) - 3;
	if (extension == "wav")
	{
		return addBufferWav(filename);
	}
	else if (extension == "ogg")
	{
		return addBufferOgg(filename);
	}
	else
	{
		LOG("Extension haven't supported yet!");
		return ERROR;
	}
}

ALuint OpenAL::getSourceId(char* filename)
{
	for (auto it = soundSourcesDict.begin(); it != soundSourcesDict.end(); it++)
	{
		if (strcmp(filename, it->second.name) == 0)
		{
			return it->first;
		}
	}
	return 0;
}

ALuint OpenAL::load(char* filename)
{
	/* Load the sound into a buffer. */
	ALuint buffer = loadSound(filename);
	if (!buffer)
	{
		return 0;
	}

	/* Create the source to play the sound with. */
	ALuint sourceId = 0;
	alGenSources(1, &sourceId);
	alSourcei(sourceId, AL_BUFFER, (ALint)buffer);

	soundSourcesDict[sourceId] = SoundBuffer{ filename, buffer };

	return sourceId;
}

void OpenAL::unload(char* filename)
{
	for (auto it = soundSourcesDict.begin(); it != soundSourcesDict.end(); it++)
	{
		if (strcmp(filename, it->second.name) == 0)
		{
			ALenum source_state;
			alGetSourcei(it->first, AL_SOURCE_STATE, &source_state);
			if (source_state != AL_PLAYING)
			{
				releaseSource(it->first);
				releaseBuffer(it->second.bufferId);

				soundSourcesDict.erase(it->first);					
			}
			return;
		}			
	}
}

void OpenAL::unloadUnused()
{
	auto it = soundSourcesDict.begin();
	while (it != soundSourcesDict.end())
	{			
		ALenum source_state;
		alGetSourcei(it->first, AL_SOURCE_STATE, &source_state);
		if (source_state != AL_PLAYING)
		{
			releaseSource(it->first);
			releaseBuffer(it->second.bufferId);

			it = soundSourcesDict.erase(it);
		}
		else
		{
			it = it++;
		}
	}
}

void OpenAL::setPositon(char* filename, float x, float y, float z)
{
	ALuint sourceId = getSourceId(filename);
	if (sourceId > 0)
	{
		setPositon(sourceId, x, y, y);
	}
}

void OpenAL::setPitch(char* filename, float pitch)
{
	ALuint sourceId = getSourceId(filename);
	if (sourceId > 0)
	{
		setPitch(sourceId, pitch);
	}
}

void OpenAL::setGain(char* filename, float gain)
{
	ALuint sourceId = getSourceId(filename);
	if (sourceId > 0)
	{
		setGain(sourceId, gain);
	}
}

void OpenAL::setRolloff(char* filename, float rolloff)
{
	ALuint sourceId = getSourceId(filename);
	if (sourceId > 0)
	{
		setRolloff(sourceId, rolloff);
	}
}

void OpenAL::init()
{


	/* Initialize OpenAL. */
	if (initAL() != true)
		return;
}

void OpenAL::release()
{
	stopAllSound();
	releaseAllSound();

	/* Release OpenAL. */
	closeAL();

	initialized = false;
}

void OpenAL::play(char* filename, bool loop)
{
	if (!isInitialized())
	{
		LOG("OpenAL need to initialize first");
		return;
	}

	ALuint sourceId = getSourceId(filename);

	if (sourceId > 0)
	{
		ALenum source_state;
		alGetSourcei(sourceId, AL_SOURCE_STATE, &source_state);
		if (source_state == AL_PLAYING)
		{
			LOG("%s is playing --- Skipped", filename);
			return;
		}
	}
	else
	{
		sourceId = load(filename);
	}

	play(sourceId, loop);
}

void OpenAL::stop(char* filename)
{
	for (auto it = soundSourcesDict.begin(); it != soundSourcesDict.end(); it++)
	{
		if (strcmp(filename, it->second.name) == 0)
		{
			stop(it->first);
		}
	}
}

void OpenAL::stopAllSound()
{
	for (auto it = soundSourcesDict.begin(); it != soundSourcesDict.end(); it++)
	{
		stop(it->first);
	}
}

void OpenAL::releaseAllSound()
{
	for (auto it = soundSourcesDict.begin(); it != soundSourcesDict.end(); it++)
	{
		releaseSource(it->first);
	}

	for (auto it = soundSourcesDict.begin(); it != soundSourcesDict.end(); it++)
	{
		releaseBuffer(it->second.bufferId);
	}

	soundSourcesDict.clear();
}