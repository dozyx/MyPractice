### Executor

Java 在 java.util.concurrent 包中引入了 Executor 框架，使用 Executor 创建工作队列只需要一行代码：

> ExecutorService exec = Executors.newSingleThreadExecutor();

接着可以提交需要执行的任务：

> exec.execute(runnable);

终止 executor：

>    exec.shutdown(); // 该方法不会等待已提交任务完成

