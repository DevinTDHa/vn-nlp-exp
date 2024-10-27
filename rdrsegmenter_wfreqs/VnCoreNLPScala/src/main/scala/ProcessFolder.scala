import vn.pipeline.{Annotation, VnCoreNLP}

import java.io.File
import java.util.concurrent.ForkJoinPool
import scala.collection.parallel.CollectionConverters.ArrayIsParallelizable
import scala.collection.parallel.ForkJoinTaskSupport
import scala.jdk.CollectionConverters._
import scala.util.Using
import java.nio.file.Paths

object ProcessFolder {

  private class Processor(inputFolder: String, outputFolder: String) {
    private val pipeline = new VnCoreNLP(Array("wseg"))

    private def processText(text: String): Seq[String] = {
      val annotation: Annotation = new Annotation(text)
      pipeline.annotate(annotation)

      annotation.getWords.asScala.map(_.getForm).toSeq
    }

    def processFile(fileName: String): Unit = {
      val absolutePath = Paths.get(inputFolder, fileName).toAbsolutePath.toString
      println(s"Processing: $fileName")
      Using.resource(scala.io.Source.fromFile(absolutePath)) { file =>
        val text: Iterator[String] = file.getLines()
        val segmented: Iterator[String] = text.map(processText(_).mkString(" "))

        // Write the segmented text to a file
        val outputFile = outputFolder + fileName.replace(" ", "_")
        Using.resource(new java.io.PrintWriter(outputFile)) {
          writer =>
            println(s"Writing to $outputFile")
            segmented.foreach(writer.println)
        }

      }
    }
  }

  def main(args: Array[String]): Unit = {
    val inputFolder = args(0)
    val outputFolder = if (args(1).endsWith("/")) args(1) else args(1) + "/"
    val numWorkers = args(2).toInt

    println("Running with args " + args.mkString(" "))

    // Create output Folder if it doesnt exist
    new File(outputFolder).mkdirs()

    val processor = new Processor(inputFolder, outputFolder)

    val alreadyProcessed = new File(outputFolder).listFiles
      .filter { f => f.isFile }
      .map(_.getName)
      .toSet

    println(s"Already processed ${alreadyProcessed.size} files")

    // List all files in the input folder
    val taskList = new File(inputFolder).listFiles
      .filter { f =>
        f.isFile && !alreadyProcessed.contains(f.getName)
      }
      .map(_.getName)
      .par

    taskList.tasksupport = new ForkJoinTaskSupport(new ForkJoinPool(numWorkers))

    println(s"Processing ${taskList.length} files")

    val startTime = System.currentTimeMillis()
    taskList.foreach(processor.processFile)
    val endTime = System.currentTimeMillis()

    println(s"Processing completed in ${(endTime - startTime) / 1000} s")
  }

}
