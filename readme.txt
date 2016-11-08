Step -2. Please take note that all the code given are done in Sequential way which can be SUPER INEFFICIENT (40+ hours rendering). What we did was to edit the output part a bit and assign different computer to do different parts of the video (in parallel).

Step -1.Before Running the code, please make sure that Opencv and Python 2.4.9 has been successfully and correctly installed such that it can successfull produce .avi video document. 

Step 0, please make sure that the 3 source videos and the field image (field.png) are in the same directory as the source code

Step 1, run stitch.py which produces out.avi, which is the side paranoma of the field. Caution, this requires around  40 hours to render, so what we did was run stitch.py in parallel: 4 computer * 1800 frames by editing the range of frame produced.

Step 2, Use the out.avi to run the backgroundExtraction.py which produces "Background.jpg" as the result.

Step 3, Use the "Background.jpg" and out.avi as input, run the subtraction.py to generate the out_sub.avi, which is the side view paranoma with background subtraction. Caution: this step is another 40-hour-step that we did in parallel by editing the frame index

Step 4, Use the out_sub.avi as the input of find_player_cc.py to generate the position of possbile player object in each frames and store them in rawtraj.txt.  This can be ineffcient and is advisable to run in parallel.

Step 5, Use the position of possbile player objects stored in rawtraj.txt as the input(we provide our parallel output in the data folder), run the track_player.py to generate 3 output text file sequence.txt sequence2.txt and sequence3.txt(last defender position). The sequence.txt gives the tracking result of the players/referees and can be taken as input of topdown.py. Run topdown.py to output "topdownview.avi" and get the running distance of each player. If we use different color schemes we get "topdownview_redblue.avi", we also give a "topdownview_traj.avi" to show the movement of the players.
The name of the input file is coded in track_player.py
f0 = open("rawtraj0-4500.txt",'r')
f1 = open("rawtraj4500-5100e.txt",'r')
f2 = open("rawtraj5100-5400.txt",'r')
f3 = open("rawtraj5400-7200.txt",'r')

Step 7, Run plane_processing.py to generate the clean football field image without any text.

Step 6, Pass sequence3.txt as the input into offside.py will produce the side view paranoma video with offside detection.

-------also we provide some other code to detect and track-------
In folder "other efforts" we have two python files to track red and blue players respectively, but due to lack of time we are unable to finish it all. The demo videos "red.avi" "blue.avi" generated are enclosed as well.

