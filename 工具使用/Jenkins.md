> 思考：Jenkins 的强大在于持续化集成、持续化分发、自动化编译、测试。持续化分发并不完全有必要。 

Jenkins 是一个持续化集成和分发系统，我们可以 web UI 页面来执行操作。

## 基本知识 

### 概念
* CI：[Continuous integration](https://en.wikipedia.org/wiki/Continuous_integration)：每天多次地将所有开发者的工作副本合并到一个主线上，通常 CI 系统会执行自动化编译。
* CD：[Continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery)：与 continuous deployment 不一样
* pipeline：全称 Jenkins Pipeline，可以理解为。。。不是很能解释。。。网站原文「is a suite of plugins which supports implementing and integrating continuous delivery pipelines into Jenkins.」，意会吧。。。大概就是实现持续化集成、分发的方式吧，类似于脚本。。。Jenkins 的 pipeline 通常定义在 Jenkinsfile 文本文件（放在代码库中）中，使用 Groovy 语言。


### 使用
>  本节为 [Jenkins Guided Tour](https://jenkins.io/doc/pipeline/tour/getting-started/)简记。

#### 安装

* Java 8 
* [Docker](https://docs.docker.com/)
* Jenkins
  * [下载](http://mirrors.jenkins.io/war-stable/latest/jenkins.war)
  * 终端执行 `java -jar jenkins.war --httpPort=8080`
  * 浏览器打开 http://localhost:8080

#### CentOS 上安装

> 自用梯子系统是 CentOS，加上自己电脑本地牌 Jenkins 没啥意思，就想要在服务器上搭一个。

参看下面教程搭建
[How to Install Jenkins on CentOS 7](https://www.vultr.com/docs/how-to-install-jenkins-on-centos-7)
需要注意的一点是，Jenkins 默认使用的是 8080 端口号，需要修改  `/etc/default/jenkins` 文件中的 `HTTP_PORT`，然后执行 `systemctl restart jenkins`，并且在上面教程的防火墙设置中启用该端口号。
教程中最后一步配置 Nginx 是可选的，配置后可以直接通过地址（不需要端口号）来访问 Jenkins，个人感觉没什么必要。

基本指令：
systemctl restart jenkins
systemctl status jenkins


> 启动 Jenkins 后在初次打开时就遇到了推荐插件装不上的问题，加上连接速度贼慢，遂放弃。

#### 创建第一个 pipeline 

* 编写 Jenkinsfile 文件，放在代码库中
* 进入 Jenkins 管理界面
* New Item -> 选择 Multibranch Pipeline -> Add Source 填写信息 -> Save
  配置完 pipeline 后，当 Jenkins 自动检测到仓库中的新分支或者新建的 pull request 时，将触发 pipeline 的运行。 

#### Jenkinsfile 文件示例（Java）

##### 简单

```
pipeline {
    agent { docker { image 'maven:3.3.3' } }
    stages {
        stage('build') {
            steps {
                sh 'mvn --version'
            }
        }
    }
}	
```

相当于执行 sh 命令

##### 多 step：每个 step 相当于一条指令

```
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'echo "Hello World"'
                sh '''
                    echo "Multiline shell steps works too"
                    ls -lah
                '''
            }
        }
    }
}	
```

##### 超时、重试、其他

```
pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                retry(3) {
                    sh './flakey-deploy.sh'
                }

                timeout(time: 3, unit: 'MINUTES') {
                    sh './health-check.sh'
                }
            }
        }
    }
}
```

##### 结束：pipeline  最后执行 post 块

```
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'echo "Fail!"; exit 1'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
```

#### 定义执行环境

上面 Jenkinsfile 文件中的 agent 告诉 Jenkins 在哪里、如何执行 Pipeline 或相关子集。所有的 pipeline 都需要有 agent。示例：

```
pipeline {
    agent {
        docker { image 'node:7-alpine' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
```

#### 环境变量

```
pipeline {
    agent any

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                sh 'printenv'
            }
        }
    }
}
```

#### 记录测试和 artifact

```
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh './gradlew build'
            }
        }
        stage('Test') {
            steps {
                sh './gradlew check'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'build/libs/**/*.jar', fingerprint: true
            junit 'build/reports/**/*.xml'
        }
    }
}
```

#### 清理和通知

```
pipeline {
    agent any
    stages {
        stage('No-op') {
            steps {
                sh 'ls'
            }
        }
    }
    post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success {
            echo 'I succeeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            echo 'I failed :('
        }
        changed {
            echo 'Things were different before...'
        }
    }
}
```

如发送邮件

```
post {
    failure {
        mail to: 'team@example.com',
             subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
             body: "Something is wrong with ${env.BUILD_URL}"
    }
}
```

#### 部署

```
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying'
            }
        }
    }
}
```



## 实践

### 集成 Android 项目

> 编译工具：gradle  

* 安装 gradle 插件，如果在搭建 Jenkins 时选择了推荐插件，会自动安装。
* 新建任务 -> 构建一个自由风格的软件项目 -> 填写信息 -> 构建中选择 invoke gradle script -> use gradle wrapper -> tasks 中可填入想要执行的任务，如 assembleRelease
  * Invoke gradle script 中，勾选 Make gradlew executable。否则会提示权限拒绝问题。
* （可选）如果工程位于 github ，需要配置，系统管理 -> github -> github servers，或者在创建任务时配置
* 配置 android sdk 路径。Jenkins 会自动从工程的 local.preperties 中读取 sdk.dir 的路径，如果没有，也可以在系统配置 -> 全局属性 -> 环境变量里添加 ANDROID_HOME 变量，值为本地 sdk 所在路径。
* 运行 unit test
* 运行 Instrument Test
* Lint



#### 上传到蒲公英

https://www.pgyer.com/doc/view/jenkins_plugin

插件上传成功后，会将蒲公英返回参数注入为 jenkins 的全局变量



#### 邮件

jenkins 配置：

* 需要配置发件人信息和服务器

task 配置：

* 配置 Triggers

参考：[jenkins配置邮件及增强版邮件通知](https://blog.csdn.net/u013066244/article/details/78665075)



#### 360 加固

编写脚本使用命令行加固

注意：

* 360 加固的 jar，mac 和 Windows 不是共用的
* 如果 360 加固文件要上传到 git 的话，需要注意 bin 文件夹是否被忽略了。。。



#### 根据参数配置执行不同的 gradle task

* General 勾选 `This project is parameterized`，并添加值，这些值可以通过环境变量访问
* 使用 `$` 使用环境变量。

比如，assemble${env}Release



### 配置branch

需要注意源码管理中需要将分支指定为分支的环境变量

#### 配置 branch Filter

正则匹配多个字符串：`^(?:.*release|.*master).*$`

> ?: 的意思是不创建 capture group。创建的 group 可以在表达式中使用 \1 的方式引用 。

参考：

https://stackoverflow.com/questions/30095583/how-do-i-configure-jenkins-to-build-all-branches-except-a-few-which-i-exclude



### 问题记录
#### github v1.26.0 is missing. To fix, install v1.26.0 or later.
确保插件已安装后，重启 Jenkins 后正常

#### The Gradle wrapper has not been found in these directories
权限问题，需要在系统设置或在任务中配置账户

#### Failed to install the following Android SDK packages as some licences have not been accepted.

[参考](https://stackoverflow.com/questions/54273412/failed-to-install-the-following-android-sdk-packages-as-some-licences-have-not-b)

window 执行 `%ANDROID_HOME%/tools/bin/sdkmanager --licenses` 没用

linux 执行 `yes | sdkmanager --licenses` 有用



#### 提示 sdk 找不到

`SDK location not found. Define location with an ANDROID_SDK_ROOT environment variable or by setting the sdk.dir path in your project's local properties file at `

确定环境变量已配置。后台帮忙在 linux 上配置的时候一直提示这个错误，后面在 Jenkins 上配置了变量才正常，很奇怪为什么他们的 Jenkins 无法读取系统的环境变量，不过也有可能是要重启 Jenkins，但他们没有帮我重启，所以不确定原因。

mac 需要注意 sdk 文件目录权限





###  忘记账号密码

谷歌搜索的答案大部分是说在 `~/.jenkins/secrets/initialAdminPassword` 可以查看，不过我没有找到该文件(Mac 系统)。最后修改了 `~/.jenkins/configs.xml` 文件，将 disableSignup 的值改为 false，重启 Jenkins 后新建账号登录。







参考：
[Configure your Android project on Jenkins](https://www.zuehlke.com/blog/en/configure-your-android-project-on-jenkins/)（不知道是不是时间太久的问题，我按照 Jenkins 官网链接的这篇文章来操作没有成功，android sdk 没能安装上，最后发现可以使用本地已有的 sdk）
[Setting Up Jenkins For Android: How I dealt with the challenges I faced](https://android.jlelse.eu/setting-up-jenkins-for-android-how-i-dealt-with-the-challenges-i-faced-1bbdb6580b8d)

