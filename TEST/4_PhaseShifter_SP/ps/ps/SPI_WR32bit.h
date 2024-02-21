#include <stdio.h>
#include <reg52.h>
#include <intrins.h>
#define uchar unsigned char
#define uint  unsigned int
#define ulong unsigned long

sbit ad9850_w_clk    =P3^0;  //P1.0�ڽ�ad9850��w_clk��/PIN7
sbit ad9850_fq_up    =P3^1;  //P1.1�ڽ�ad9850��fq_up��/PIN8
sbit ad9850_rest     =P3^2;  //P1.2�ڽ�ad9850��rest��/PIN12
sbit ad9850_bit_data =P3^3;  //P1.3�ڽ�ad9850��D7��/PIN25

//ad9850��λ(����ģʽ)
void ad9850_reset_serial()
{
	ad9850_rest=0;
	ad9850_bit_data=0;
	ad9850_fq_up=0;
	ad9850_w_clk=0;
}

//��ad9850��д����������(����)
void ad9850_wr_serial(ulong dress,ulong data1)
{
	uchar i;
	ulong w, y;

	y=data1;

	ad9850_rest=1;
	ad9850_fq_up=1;

    //дdress����
	w=dress;   
		for(i=0;i<3;i++)
	{
		ad9850_bit_data=0;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}
		ad9850_bit_data=0;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
		ad9850_bit_data=1;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	for(i=0;i<4;i++)
	{
		ad9850_bit_data=(w<<i)&0x8;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}
		ad9850_bit_data=w&0x01;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
		ad9850_fq_up=0;
		ad9850_bit_data=w&0x01;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
		ad9850_fq_up=1;

	   	w=dress;   
		for(i=0;i<2;i++)
	{
		ad9850_bit_data=0;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}




	//дw4����
	w=(y<<=0);
	for(i=0;i<8;i++)
	{
		ad9850_bit_data=(w<<i)&0x80000000;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}
	//дw3����
	w=(y<<8);
	for(i=0;i<8;i++)
	{
		ad9850_bit_data=(w<<i)&0x80000000;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}
	//дw2����
	w=(y<<16);
	for(i=0;i<8;i++)
	{
		ad9850_bit_data=(w<<i)&0x80000000;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}
	//дw1����
	w=(y<<24);
	for(i=0;i<8;i++)
	{
		ad9850_bit_data=(w<<i)&0x80000000;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
	}

	    ad9850_bit_data=0;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
		ad9850_fq_up=0;
		ad9850_bit_data=0;
		ad9850_w_clk=1;
		ad9850_w_clk=0;
		ad9850_fq_up=1;

}
