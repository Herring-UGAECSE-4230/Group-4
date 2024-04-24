OBJS = BIT_BANG.o
ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
GPIO_OFF: $(OBJS)
	gcc -o BIT_BANG $(OBJS)

clean:
	rm *.o BIT_BANG
