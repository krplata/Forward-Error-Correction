--------------- Forward Error Correction ---------------
Authors: Krystian Plata, Konrad Olszewski	       |
Project deadline: Jul 18, 2018			       |
--------------------------------------------------------
Tools used:					       |
- Pycharm (Python IDE)				       |
- Online image comparison tool available at:	       |
https://www.imgonline.com.ua/eng/similarity-percent.php|
---------------------------------------------------------------------------------
Project Description:							        |
									        |
This implementation is a result of a university course:			        |
	"Reliability and Diagnostics of Digital Systems"		        |
									        |
The group was to provide an implementation of the following:		        |
- BSC nad Gilbert channels						        |
- Error correction codes: TMR, Hamming(8,4), Reed-Solomon		        |
- Interlacing as a tool to break up big chunks of error bits into smaller groups|
---------------------------------------------------------------------------------
The outline of a main algorithm of result checking:				|
										|
1) Prepare the input file.							|
2) Send it through a selected channel.						|
3) Use a selected correction code to retrieve the original image.		|
4) Compare the results with an image comparison tool.				|
---------------------------------------------------------------------------------
Each channel is characterized by a set of attributes:				|
- Binary Symetric Channel:							|
	+ p - Probability of error occurence					|
- Gilbert:									|
	- p_gb - Probability of state switching: good -> bad			|
	- p_bg - Probability of state switching: bad -> good			|
---------------------------------------------------------------------------------
Sample results of error correction are stored in the Images folder.		|
---------------------------------------------------------------------------------
Imported libraries are stated in a generated requirements.txt file.		|
---------------------------------------------------------------------------------

