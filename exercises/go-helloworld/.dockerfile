# use the golang:alpine base image
FROM golang:alpine

# set the working directory to /go/src/app
WORKDIR /go/src/app 

# import dependencies using `go mod init` and build the application using `go build -o helloworld` command, where `-o helloworld` will create the binary of the application with the name `helloworld`
ADD . . 

# import dependencies using `go mod init` and build the application using `go build -o helloworld` command
RUN  go mod init && go build -o helloworld

# expose the port 6111
EXPOSE 6111

# start the container
CMD ["./helloworld"]