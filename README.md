# Build a Modern Computer from First Principles: From Nand to Tetris I & II

Absolutely amazing course available at https://www.nand2tetris.org/. 

I must say that this course constructed by both Shimon Schocken and Noam Nisan is nothing short of phenominal. Cant recommend this enough to people who just want to understand how all the magic "black box abstractions" of the modern computer work.

For a while I have had hobby projects involving retro hardware, and seen many recommendations from people online that this was a really fun course. I can now officially say that it is completely true!

We are tasked with building the "Hack" computer from scratch, starting with building the actual computer out of basic logic chips. Following this we move on to building our own assembler, VM translator and even a compiler for the high level java-like Jack language. 

Below is a brief description of the projects, and also you can find my solutions to course problems in this repository with links below. I have done my implementations in <ins>Python</ins>

## Project 1 to 3

Key focus here was building basic chips out of low level gates. Project 1 focused on building each of the base logic chips starting with a Nand gate, moving up to memory.
It was interesting to build and form the basis of a 16 full adder, 16 bit registers which make up the structure of a ROM/RAM and also building a program controller. This was all done using a specification of HDL.

## Project 4

This project focuses on the building of programs using the Hack assembly language. We were required to build 2 programs that focused on manipulating ram, the virtual screen and all using inputs from a virtual keyboard.

## Project 5

Time to put everything together. This unit was about combinining all knowledge gained prior, into building the CPU, RAM, and Computer. This computer can execute the instructions provided by the Hack assembly. 

## Project 6

Enter more software! We pulled everything together and were required to write our own assembler for the Hack computer. I decided to use Python for this part of the course as its a language I had some experience in.

[py-assember](https://github.com/scassar/nand2tetris/tree/master/projects/06/py-assembler)

## Project 7

First part of 2 which is about creating our own stack based VM translater for the bytecode of the Jack language. Simple mapping converter into Hack assembly. This can be accessed at the below link. I have not linked project 7 here but you can see the full VM Translator located at the link for project 8.

## Project 8 

This was a an exciting ride figuring out how to write the assembly code to do the function, call and return commands. If anything is certain, this project highlights how simple (and complex) a stack based VM implementation can be. Further optimisations to follow as the code currently is very verbose (I thought easier to keep the instructions clear)

[py-vmtranslator](https://github.com/scassar/nand2tetris/tree/master/projects/08/py-vm)

## Project 9

Wait what?! finally we are back to a high level programming language *clap*. Here we learnt about the Jack language for which we will build a compiler in projects 10 and 11. I decided to write a small implementation of my GBA game Escape the Godfather (ETG). Check it out below!

[ETG](https://github.com/scassar/nand2tetris/tree/master/projects/09)

## Project 10

Okay things are getting really tough now. Project 10 has us build 50% of the compiler through starting with the lexical and syntax analyser. This is tough because you need to parse all the tokens in the original Jack file, and produce an XML file mapping all elements for testing. This is highly recursive (I am never going to under estimate this again), but overall was a really intense challenge. Looking forward to completing the generator component. You can checkout part 10 below. (Note: I am planning to come back and add additional error handling in the future)

[Jack-Analyzer](https://github.com/scassar/nand2tetris/tree/master/projects/10)

## Project 11 

Finished! Now I would prefer never to do that again (jokes!). Absolutely sensational feeling to complete the entire compiler. I was able to get each of the programs supplied by the course running, and even used it to compile my own Escape the Godfather game from project 9. This challenge required learning about the role of symbol tables in compilers, and dealing with the nature of the VM generation being recursive. Highly recommend everyone doing this course to attempt and complete this project. You can find my Jack Compiler solution below: 

[Jack-Compiler](https://github.com/scassar/nand2tetris/tree/master/projects/11)

## Project 12

Well folks, thats a wrap! This module required us to implement many of the functions we had taken for granted throughout this course. Many modules such as Sys, Math, Memory and Array etc are required in order to build properly functioning Jack programs. This was actually a very challenging part of the course for me, as its been many years since I whipped out an old notepad to do some math. 

## Summary

I am a little sad that the course is over, as it was brilliant from start to finish. Fortunately, given this domain there is always more enhancements that can be made! I will give this project a break for now as I am next looking to focus on FPGA tech and other 6502 projects. Still - This was one of the best courses I have ever completed!

## Nand2Tetris artefacts  

### Overall

![image](https://github.com/scassar/nand2tetris/assets/2356898/5172cb52-d531-40a1-9457-b8f30163cb28)

**Nand2Tetris CPU overall schematic**

![image](https://github.com/scassar/nand2tetris/assets/2356898/db3ec066-99c1-45b3-85fc-b404866fe7f7)

**Nand2Tetris VM memory map**
![image](https://github.com/scassar/nand2tetris/assets/2356898/1f04a508-8a7d-4da6-b78d-89dc9e9f4734)
