% Define parameters for audio recording
fs = 16000;        
nBits = 16;        
nChannels = 1;     
recordTime = 2;    
recObj = audiorecorder(fs, nBits, nChannels);

% Define parameters for file storage
test_train = "train";
osoba = "p1";
num_rec = 10;
command = "vyhodne";



for i = 1:num_rec
    filePath = pwd + "\data\" + test_train + "\" + osoba + "\" + command + "\" + "r_" + i + ".wav";
    
    disp(['Start speaking: ' command]);
    recordblocking(recObj, recordTime);
    disp('End of Recording.');
    audioData = getaudiodata(recObj);
    audiowrite(filePath, audioData, fs);
    
    % Plot the audio data
    timeAxis = linspace(0, recordTime, length(audioData));
    plot(timeAxis, audioData);
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(['Audio Signal - Recording ' num2str(i)]);
    
    play(recObj);    
    input('Press Enter to continue to the next recording.', 's');
end
