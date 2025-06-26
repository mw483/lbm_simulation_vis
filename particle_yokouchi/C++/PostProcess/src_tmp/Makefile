# Makefile
#CC 			= g++
CC			= nvcc
CFLAGS 	= -O3 -g -Xcompiler -fopenmp
LDFLAGS =
LIBS 		=

TARGET 	= run_analysis
SRCS 		= main.cu
include SourceList.mak

OBJS    = 	$(filter %.o,$(SRCS:%.cpp=%.o))
OBJS		+=	$(filter %.o,$(SRCS:%.cu=%.o))

%.o:%.cpp
					$(CC) $(CFLAGS) -c $^

%.o:%.cu
					$(CC) $(CFLAGS) -c $^

all:$(TARGET)

$(TARGET):$(OBJS)
					$(CC) $(CFLAGS) -o $@ $(OBJS)

clean:
	rm -f *.o
	rm -f $(TARGET)
