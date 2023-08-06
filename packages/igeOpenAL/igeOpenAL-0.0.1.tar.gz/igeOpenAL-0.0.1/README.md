# igeOpenAL

C++ extension OpenAL sound for 3D and 2D games.

You can install it using the PyPI:

	pip install igeOpenAL

### Features
- (ogg , wav) extension are supported
- Preload supported

### Functions
# First, you need to import and init the firebase system
```python
import pyxopenal

sound = pyxopenal.sound()
sound.init()
```

# Play the sound
```python
# (sound_name , loop)
sound.play('sound/beep2.ogg', False)
```
# Release it when everything is done
```python
sound.release()
```
# 3D sound optional
- Global
```python
# (option)
sound.setListenerPosition(0, 0, -10);
sound.setListenerOrientation(0, 0, -10, 0, -1.0, 0);
```
- Local
```python
# (sound_name , option)
sound.setPositon('sound/beep2.ogg', 0, 0, -10);
sound.setPitch('sound/beep2.ogg', 1.1);
sound.setGain('sound/beep2.ogg', 1.1);
sound.setRolloff('sound/beep2.ogg', 1.1);
```

### Todo
- To support streaming
- Sound packing strucure

### Reference
- [OpenAL](https://www.openal.org/)
- [OpenAL Soft](https://github.com/kcat/openal-soft) - a software implementation of the OpenAL 3D audio API.
- [Xiph](https://xiph.org/) - Ogg loader

