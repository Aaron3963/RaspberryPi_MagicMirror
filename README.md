# Magic-Mirror-with-RaspberryPi
What it can do
----------------------------------
    This project is trying to imitate the magic mirror in the movie *SnowWhite*
    The project will remain in silence when there is no one arround
    When someone stands infront of it for some time, it will wake up and "talk" to him/her
    When the person leaves, the mirror go back to rest
How it works
----------------------------------
    System booted
    Program starts to run automatically
    Monitor displaying wallpaper, webcam scaning for faces
    
    If Face detected, wake the main method
        Display footage from webcam, using squares to point out eyes, mouth and the whole face
    
        If the face continues to stay in site(50 frames), play:"请说话"（"Please speak"）, microphone starts to record
            Voice recognition translate record to text
            Turing AI gives out the answer
            Voice generation translate text from Turing to record
            Play record
                
                If the text from user contains"唱一首歌"("Please sing a song"), randomly play music
        
        else, return to displaying wallpaper
   
   else, return to displaying wallpaper
    
    
Hardware:
----------------------------------  
Raspberry Pi (I am using 3B)
> 
Monitor
> 
Speakers
> 
Webcam & microphone

Software:
----------------------------------  
The installation of OpenCV is needed
> 
[Best tutorial for OpenCV installation I've ever met, huge thanks to the author]( https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)<br /> 
> 
Voice generation & recognition is essential, I used it from Baidu but you can also use other sources
> 
[URL to Baidu Voice recognition]( http://ai.baidu.com/tech/speech)<br />  
> 
[URL to Baidu Voice generation]( http://ai.baidu.com/tech/speech/tts)<br />  
> 

The conversation AI is used from Turing, other sources may work too.
> 
[URL to Turing robot]( http://www.turingapi.com/)<br />    

More about:
----------------------------------
My email adress: **Aaron3963@163.com**

