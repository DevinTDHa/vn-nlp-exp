# Scala Program to run VnCoreNLP concurrently

Requirements:

1. sbt and scala installed
2. [`VnCoreNLP-1.2.jar`](https://github.com/vncorenlp/VnCoreNLP) in the `lib/` folder

Then you can run `sbt assembly` to build a jar and run it. Usage of the program:

```bash
java -jar target/scala-2.13/VnCoreNLPScala-assembly-0.1.0-SNAPSHOT.jar  <input-file> <output-file> <num-workers>
```

where num-workers is the number of workers you want to run concurrently.
