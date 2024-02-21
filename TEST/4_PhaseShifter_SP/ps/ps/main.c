																													 #include<LQ12864.h>
#include<reg52.h>
#include<stdio.h>
#include <string.h>
#include<SPI_WR32bit.h>

/*
sbit zuo=P1^5;
sbit you=P1^1;
sbit shang=P1^6;
sbit xia=P1^0;
sbit yes=P1^4;
*/


sbit zuo=P1^3;
sbit you=P1^4;
sbit shang=P1^1;
sbit xia=P1^2;
sbit yes=P1^5;

void main()
{
  ulong data0=0x00000000,data1=0x00000001,data2=0x00000002,data3=0xffffffff,data4=0x0bcfaaaa,data5=0x00000000,data6=0x80101010,data7=0x00000001,datatem,PSI1,PSQ1;
  int num=1,flag=0, reg=0,i=0,PSI=0,PSQ=1,w;
  char str_reg[10],str_data[10],str_data_0x[10];
  OLED_Init();
  Draw_BMP(0,0,128,7,BMP1);
  delay(2000);
  delay(2000);
  delay(2000);
  delay(2000);
  delay(2000);
  OLED_Init();
  ad9850_reset_serial();
  OLED_P6x8Str(15, 5,"*");
  OLED_P6x8Str(15, 2,"I:");
  OLED_P6x8Str(68, 2,"Q:");
  while(1)
  {
  	  if(zuo==0||you==0||shang==0||xia==0)
   		{
		   if(zuo==0||you==0||shang==0||xia==0)
   		{
		   if(you==0)
  			{
   				while(you==0);
  					num++;
				if(num<1)
  	 				num=2;
  				if(num>2)
  	 				num=1;
	 			switch (num)
  				{
   					case 1:
						OLED_P6x8Str(15, 5,"*");
						OLED_P6x8Str(68, 5," ");
						break;
   					case 2:
					    OLED_P6x8Str(15, 5," ");
						OLED_P6x8Str(68, 5,"*");
						break;
				}

	    	 }

			 if(zuo==0)
  			{
   				while(zuo==0);
  					num--;
				if(num<1)
  	 				num=2;
  				if(num>2)
  	 				num=1;
	 			switch (num)
  				{
   					case 1:
						OLED_P6x8Str(15, 5,"*");
						OLED_P6x8Str(68, 5," ");
						break;
   					case 2:
					    OLED_P6x8Str(15, 5," ");
						OLED_P6x8Str(68, 5,"*");
						break;
				}

	    	 }


				 	if(shang==0)
  			{
   				while(shang==0);
	 			switch (num)
  				{
  					case 1:
					PSI++;
					break;
					case 2:
					PSQ++;
					break;
  				}
  			}

				if(xia==0)
  			{
   				while(xia==0);
	 			switch (num)
  				{
  					case 1:
					PSI--;
					break;
					case 2:
					PSQ--;
					break;
  				}
  			}


		   }

		   if(flag==0)
   			{	
				OLED_P6x8Str(60,0,"  ?");
				flag=1;
   			}
 	  
          }

		   if(PSI<0)
  	 		PSI=63;
  			if(PSI>63)
  	 		PSI=0;
			if(PSQ<0)
  	 		PSQ=63;
  			if(PSQ>63)
  	 		PSQ=0;


		  sprintf(str_data_0x,"%2d",PSI);
	      OLED_P6x8Str(15, 4,str_data_0x);
		  sprintf(str_data_0x,"%04lx",PSI1);
	      OLED_P6x8Str(15, 6,str_data_0x);

		  sprintf(str_data_0x,"%2d",PSQ);
		  OLED_P6x8Str(68, 4,str_data_0x);
		  sprintf(str_data_0x,"%04lx",PSQ1);
		  OLED_P6x8Str(68, 6,str_data_0x);

		  PSI1=PSI%2*1+(PSI%2==0)*2+PSI/2%2*4+(PSI/2%2==0)*8+PSI/4%2*16+(PSI/4%2==0)*32+PSI/8%2*64+(PSI/8%2==0)*128+PSI/16%2*256+(PSI/16%2==0)*512+PSI/32%2*1024+(PSI/32%2==0)*2048;
		  PSQ1=PSQ%2*1+(PSQ%2==0)*2+PSQ/2%2*4+(PSQ/2%2==0)*8+PSQ/4%2*16+(PSQ/4%2==0)*32+PSQ/8%2*64+(PSQ/8%2==0)*128+PSQ/16%2*256+(PSQ/16%2==0)*512+PSQ/32%2*1024+(PSQ/32%2==0)*2048;
		  data0= (PSQ1<<12)+ PSI1+0xff000000;

		  	
			

		  if(yes==0)
	 	    {
	  		 while(yes==0);	
		     OLED_P6x8Str(60, 0,"OK!");		 
	   		 flag=0;

			 ad9850_fq_up=0;
			 ad9850_rest=0;
			 delay(200);
			 ad9850_fq_up=1;
			 ad9850_rest=1;	
				
			 ad9850_wr_serial(0,data0);
			 ad9850_wr_serial(1,data1);
			 ad9850_wr_serial(2,data2);
			 ad9850_wr_serial(3,data3);
			 ad9850_wr_serial(4,data4);
			 ad9850_wr_serial(5,data5);
			 ad9850_wr_serial(6,data6);
			 ad9850_wr_serial(7,data7);
		   w=0x10;   
		for(i=0;i<8;i++)
	{
		ad9850_bit_data=(w<<i)&0x80;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}	 

		ad9850_bit_data=1;
		ad9850_w_clk=1;
		ad9850_w_clk=0;

        ad9850_bit_data=1;
		ad9850_w_clk=1;
		ad9850_w_clk=0;

		ad9850_fq_up=0;
		ad9850_bit_data=1;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
		ad9850_fq_up=1;	

		for(i=0;i<100;i++)
	{
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}					   //

	   delay(200);

	 	    }
   }
}



