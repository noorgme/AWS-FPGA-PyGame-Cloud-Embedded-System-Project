#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>

#define OFFSET 						  -32
#define JTAG_DATA_REG_OFFSET          0
#define JTAG_CNTRL_REG_OFFSET         1
#define JTAG_UART_RV_BIT_MASK         0x00008000
#define JTAG_UART_DATA_MASK           0x000000FF
#define FILTER_SIZE					  25

volatile alt_u32* uartDataRegPtr = (alt_u32*)JTAG_UART_BASE;
volatile alt_u32* uartCntrlRegPtr = (alt_u32*)JTAG_UART_BASE + JTAG_CNTRL_REG_OFFSET;

alt_32 x_read;
alt_32 y_read;
alt_32 z_read;
alt_32 x_filter;
alt_32 y_filter;
alt_32 z_filter;
alt_u8 RECV_CHAR;
alt_u8 RECV_FLAG = 0;
alt_u32 FILTER_HEAD = 0;
const alt_32 FILTER_TAPS[FILTER_SIZE] = {302,485,-158,-466,217,7,-617,263,289,-872,197,748,-1174,-73,
										1462,-1475,-715,2596,-1724,-2216,4929,-1894,-7891,18868,41740};
										//18868,-7891,-1894,4929,-2216,-1724,2596,-715,-1475,1462,-73,
										//-1174,748,197,-872,289,263,-617,7,217,-466,-158,485,302};


alt_u32 uart_checkRecvBuffer(alt_u8* byte){
	alt_u32 return_val;
	alt_u32 DataReg = *uartDataRegPtr;
	*byte = (alt_u8)(DataReg & JTAG_UART_DATA_MASK);
	return_val = DataReg & JTAG_UART_RV_BIT_MASK;
	return_val = return_val >> 15;
	return return_val;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    if(!RECV_FLAG){
    	RECV_CHAR = alt_getchar();
    	RECV_FLAG = 1;
    }
}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0xF000);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

void filter(alt_32 buffer[3][FILTER_SIZE], alt_32 x_read,alt_32 y_read,alt_32 z_read,alt_32 *x_filter,alt_32 *y_filter,alt_32 *z_filter){
	*x_filter = 0;
	*y_filter = 0;
	*z_filter = 0;
	buffer[0][FILTER_HEAD] = x_read;
	buffer[1][FILTER_HEAD] = y_read;
	buffer[2][FILTER_HEAD] = z_read;
	for(int i=0; i<FILTER_SIZE;i++){
		*x_filter += buffer[0][FILTER_HEAD+i % FILTER_SIZE] * FILTER_TAPS[i];
		*y_filter += buffer[1][FILTER_HEAD+i % FILTER_SIZE] * FILTER_TAPS[i];
		*z_filter += buffer[2][FILTER_HEAD+i % FILTER_SIZE] * FILTER_TAPS[i];
	}
	// Fixed point scaling factor of 2^16
	*x_filter = *x_filter / 65536;
	*y_filter = *y_filter / 65536;
	*z_filter = *z_filter / 65536;
	FILTER_HEAD = (FILTER_HEAD + 1) % FILTER_SIZE;
}

int main() {

	alt_32 FILTER_BUFFER[3][FILTER_SIZE];

    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }
    timer_init(sys_timer_isr);
    while (1) {

        alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
        alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
        alt_up_accelerometer_spi_read_z_axis(acc_dev, & z_read);
        filter(FILTER_BUFFER,x_read, y_read, z_read,&x_filter,&y_filter,&z_filter);
        alt_printf("[%x,%x,%x]\n",x_filter,y_filter,z_filter);
        // Char received over UART
        alt_printf("%x",RECV_CHAR);
        if(RECV_FLAG){
        	if(RECV_CHAR == 'V'){
        		alt_printf("[%x,%x,%x]\n",x_filter,y_filter,z_filter);
        	}
        	RECV_FLAG = 0; //Reset flag to wait for next receive
        }
    }

    return 0;
}

