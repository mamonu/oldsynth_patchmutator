/***************************************************************/
/* This short program prepares a 4096 byte DX7 voice dump file */
/* for transmission as a system exclusive message via MIDI.    */
/* The output file should be sent, byte-for-byte, over MIDI    */
/* to the DX7 (or compatible synth).  All information,         */
/* including the header, checksum, and trailer are added.      */
/* Written by:  Gary Snethen (xeno@iastate.edu)   11/7/93      */
/***************************************************************/

#include <stdio.h>

int main(int argc, char *argv[])
{

  unsigned char buffer[4200];


  FILE *input, *output;
  int checksum, i;

  if (argc != 3 || !strcmp("-h",argv[1]) || !strcmp("-h",argv[2])) {
    printf("%s prepares a 4096 byte DX7 voice dump for MIDI transmission.\n",
      argv[0]);
    printf("usage: %s <input file> <output file>\n",argv[0]);
    exit(0);
  }

  input = fopen(argv[1],"rb");
  output = fopen(argv[2],"wb");

  if (!input)
    printf("%s error: cannot open %s for reading!\n", argv[0], argv[1]);
  if (!output)
    printf("%s error: cannot open %s for writing!\n", argv[0], argv[2]);
  if (!input || !output) exit(0);
  if (fread(buffer+6, 1, 4096, input) < 4096) {
    printf("%s error: %s is less than 4096 bytes!\n", argv[0], argv[1]);
    exit(0);
  }

/* compute checksum */
  checksum = 0;
  for (i=0; i< 4096; i++) {
    checksum += buffer[i+6];
  }

/* header for a 32 packed voice DX7 sys-ex packet */
  buffer[0] = 0xf0;  /* sys-ex */
  buffer[1] = 0x43;  /* Yamaha */
  buffer[2] = 0x00;  /* substatus=0, device=0 */
  buffer[3] = 0x09;  /* packed 32 voice format */
  buffer[4] = 0x20;  /* MSB (upper 7 bits) of data packet length (4096) */
  buffer[5] = 0x00;  /* LSB (lower 7 bits) of data packet length (4096) */

/* the DX7 expects the 2's complement with the high bit stripped off */
  buffer[4096+6] = (~checksum + 1) & 0x7f;

/* end-of-system-exclusive byte */
  buffer[4096+7] = 0xf7;

/* we have the full sys-ex packet, so we can write it out */
  if (fwrite(buffer, 1, 4104, output) < 4096) {
    printf("%s error: could not write to %s!\n", argv[0], argv[2]);
    exit(0);
  }
  printf("File successfully converted.\n");
}
