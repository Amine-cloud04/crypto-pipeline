ThisBuild / scalaVersion := "2.12.18"
ThisBuild / version      := "0.1.0"

lazy val root = (project in file("."))
  .settings(
    name := "ecommerce-pipeline",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % "3.2.4",
      "org.apache.spark" %% "spark-sql"  % "3.2.4",
      "org.apache.spark" %% "spark-sql-kafka-0-10" % "3.2.4",
      "org.elasticsearch" %% "elasticsearch-spark-30" % "8.10.2",
      "org.slf4j" % "slf4j-simple" % "1.7.36"
    )
  )
