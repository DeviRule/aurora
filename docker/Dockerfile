FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && \
    apt install -y build-essential git sudo python3 wget curl neovim htop \c
	ruby bison cmake

ARG USER_UID=1000
ARG USER_GID=1000

#Enable sudo group
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
WORKDIR /tmp

RUN useradd -m -s /bin/bash user 
#Enable sudo group
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/user
WORKDIR "/home/user"
USER user


RUN wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/sh \
  && echo source ~/.gdbinit-gef.py >> ~/.gdbinit


#################################################################
# Clone Aurora repository and prepare environment
RUN mkdir aurora
COPY --chmod=0777 .. /home/user/aurora

RUN mkdir evaluation

ENV AURORA_GIT_DIR=/home/user/aurora
ENV EVAL_DIR=/home/user/evaluation
ENV AFL_DIR=$EVAL_DIR/AFLplusplus
ENV AFL_WORKDIR=$EVAL_DIR/afl-workdir

WORKDIR $EVAL_DIR
RUN mkdir -p $EVAL_DIR/inputs/crashes && mkdir -p $EVAL_DIR/inputs/non_crashes

#################################################################
# Modify it so that it install AFL++
RUN sudo apt-get update
RUN sudo apt-get install -y build-essential python3-dev automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools cargo libgtk-3-dev wget vim lsb-release software-properties-common gnupg patch 
# try to install llvm 14 
RUN wget https://apt.llvm.org/llvm.sh
RUN sudo chmod +x llvm.sh
RUN sudo ./llvm.sh 14 all
RUN sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev

#RUN wget -q -c https://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz && tar xf afl-latest.tgz && mv afl-2.52b afl-fuzz
#Get AFL++ 
WORKDIR $EVAL_DIR
RUN touch arguments.txt
RUN git clone https://github.com/DeviRule/AFLplusplus

##  apply patch & build
RUN cd AFLplusplus/ && patch -p1 <  ${AURORA_GIT_DIR}/crash_exploration/aurora_afl.patch && make all && sudo make install

#################################################################
# Build mruby target
# RUN git clone https://github.com/mruby/mruby.git && cd mruby && git checkout 88604e39ac9c25ffdad2e3f03be26516fe866038
# ## build afl version
# RUN CC=$AFL_DIR/afl-gcc printenv | grep CC
# RUN cd mruby && CC=$AFL_DIR/afl-gcc make -e -j && mv ./bin/mruby ../mruby_fuzz

# clean
# RUN cd mruby && make clean

# build normal version for tracing/rca
# RUN cd mruby && CFLAGS="-ggdb -O0" make -e -j && mv ./bin/mruby ../mruby_trace

#################################################################
# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -q -y --default-toolchain nightly
ENV PATH="/home/user/.cargo/bin:${PATH}"


#################################################################
# Install Pin
RUN wget -q -c http://software.intel.com/sites/landingpage/pintool/downloads/pin-3.15-98253-gb56e429b1-gcc-linux.tar.gz && tar -xzf pin*.tar.gz
ENV PIN_ROOT="/home/user/evaluation/pin-3.15-98253-gb56e429b1-gcc-linux"

RUN mkdir -p "${PIN_ROOT}/source/tools/AuroraTracer" && cp -r ${AURORA_GIT_DIR}/tracing/* ${PIN_ROOT}/source/tools/AuroraTracer

## requires PIN_ROOT to be set correctly
RUN cd ${PIN_ROOT}/source/tools/AuroraTracer && make obj-intel64/aurora_tracer.so


#################################################################
# Complete setting up evaluation directory
# RUN cp $AURORA_GIT_DIR/example.zip $EVAL_DIR && unzip -q example.zip && cp -r example/mruby_type_confusion/seed .
# RUN echo "@@" > arguments.txt

#################################################################
# link clang++14 to clang++ 
RUN cd /usr/bin && sudo ln -s clang++-14 clang++

WORKDIR /home/user
