DMD = /opt/d/osx/bin/dmd
DFLAGS = -O -release -lib
INCLUDES = -I/opt/d/src/phobos -I/opt/d/src/druntime/import
LIBS = -L-L/opt/d/osx/lib -L-lcurl
TARGET = bucho.a

all: $(TARGET)

$(TARGET): bucho.d
	$(DMD) $(DFLAGS) $(INCLUDES) $(LIBS) bucho

clean:
	rm -f $(TARGET)
