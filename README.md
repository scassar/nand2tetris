# Build a Modern Computer from First Principles: From Nand to Tetris I & II

Absolutely amazing course available at https://www.nand2tetris.org/. 

Building the Hack computer by scratch using logic gates is a great experience for those who enjoy learning about low level hardware.

Below is a brief description of the projects, and also you can find my solutions to course problems in this repository.

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

Okay things are getting really tough now. Project 10 has us build 50% of the compiler through starting with the lexical and syntax analyser. This is tough because you need to parse all the tokens in the original Jack file, and produce an XML file mapping all elements for testing. This is highly recursive (I am never going to under estimate this again), but overall was a really intense challenge. Looking forward to completing the generator component. You can checkout part 10 below:

[Jack-Analyzer](https://github.com/scassar/nand2tetris/tree/master/projects/10)

## Project 11 

Finished! Now I would prefer never to do that again (jokes!). Absolutely sensational feeling to complete the entire compiler. I was able to get each of the programs supplied by the course running, and even used it to compile my own Escape the Godfather game from project 9. This challenge required learning about the role of symbol tables in compilers, and dealing with the nature of the VM generation being recursive. Highly recommend everyone doing this course to attempt and complete this project. You can find my Jack Compiler solution below: 

[Jack-Compiler](https://github.com/scassar/nand2tetris/tree/master/projects/11)

## Nand2Tetris artefacts  

**Overall**

![image](https://github.com/scassar/nand2tetris/assets/2356898/ff7392c2-dc8d-4969-92b1-d666ed5a8e55)


**Nand2Tetris CPU overall schematic**

![image](https://github.com/scassar/nand2tetris/assets/2356898/db3ec066-99c1-45b3-85fc-b404866fe7f7)

**Nand2Tetris VM memory map**
![image](https://github.com/scassar/nand2tetris/assets/2356898/1f04a508-8a7d-4da6-b78d-89dc9e9f4734)
