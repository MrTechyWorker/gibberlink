# 📂 GibberLink [For Pythonista!]

Having inspired by the viral gibberlink mode video : 

[![Agents switching from english to gibberlink mode](https://img.youtube.com/vi/EtNagNezo8w/maxresdefault.jpg)](https://www.youtube.com/watch?v=EtNagNezo8w)

I've created this simple python package that uses basic mathematics and fourier transforms to convert strings to gibber frequency sounds and play them, along with the reverse transformations to listen to the sounds and decode as strings back.

## How to Install

### Using PIP

To install the package using pip,

```bash
pip install "git+https://github.com/MrTechyWorker/gibberlink.git"
```

### Using Setuptools
To install the package using setuptools,

```python
from setuptools import setup, find_packages

setup(
    name="foo",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "gibberlink @ git+https://github.com/MrTechyWorker/gibberlink.git"
    ] 
)
```

### Using `pyproject.toml`
To install the package using toml,

```toml
[project]
dependencies = [
    "gibberlink @ git+https://github.com/MrTechyWorker/gibberlink.git"
]
```

## How to use

### Talker:

Directly import the package and use the Talker to instantiate and use the talk method

```python 
from gibberlink import Talker

talker = Talker(debug_mode = True, message_end_char = "*")
talker.talk('Hello')
```
Talker object takes 2 optional keyword arguments:

 - debug_mode : bool = This will log and show each encoded bit's frequency. Debug mode is basically to show more info on execution.

 - message_end_char : str = This is the character which will denote the end of any message you pass to the talk method. Talker obj will itself append the escape sequence when transmitting each message. 

 ### Listener:

Instantiate Listener in the same way as Talker and use the listen method to detect gibber frequencies and return the string when done.

```python 
from gibberlink import Listener

listener = Listener(debug_mode = True, message_end_char = "*")
message : str = listener.listen()
print(message)
```
The Listener object will receive the same arguments as the Talker.

```listener.listen()``` will start listening over the microphone for signals and will halt and return the decoded string when detected the ```message_end_char```.

## Code Notes:

1. Make sure the ```message_end_char``` for both the listener and talker remains the same.
2. Any interruption to the connected audio devices like unplugged or corrupted while the code is running leads to an unhandled error and program crashes.
3. Both the Talker and Listener can be used in the same program without any issue.

## 🟥 Developer Notes

1. This package is completely a starting point in which more research to be done for better performance.

2. Currently frequencies for all bit mapping are fixed. Users are encouraged to use the package source code to make it more independent of configs.

3. Since this package uses built-in microphone and speakers, it is more vulnerable to be altered/disturbed by device quality or the surround noise. Use of gibberlink with this python package shall be carried out in an isolated environment.

4. To understand core concepts of gibberlink, here are the concepts needed:
   - STFT - Short Time Fourier Transform
   - Frequency Resolution
   - Basic Digital Signal Processing
   - Sampling & Waveforms
   - Python Libraries – numpy, sounddevice, scipy
