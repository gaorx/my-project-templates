
default_kotlin_version = '1.4.31'
default_springboot_version = '2.4.4'


README = "# {{name}}\n\n {{desc}}\n"

SETTINGS_GRADLE = """
rootProject.name = '{{name}}'
"""

BUILD_GRADLE = """
plugins {
  id 'org.springframework.boot' version '{{springboot_version}}'
  id 'io.spring.dependency-management' version '1.0.11.RELEASE'
  id 'java'
  id 'org.jetbrains.kotlin.jvm' version '{{kotlin_version}}'
}

group = '{{group}}'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = '{{source_compatibility}}'

tasks.withType(org.jetbrains.kotlin.gradle.tasks.KotlinCompile).all {
  kotlinOptions {
    jvmTarget = '{{kotlin_jvm_target}}'
    freeCompilerArgs = ['-Xjsr305=strict']
  }
}

repositories {
  maven { url 'https://maven.aliyun.com/repository/gradle-plugin'  }
  maven { url 'http://maven.aliyun.com/nexus/content/groups/public' }
  maven { url 'http://maven.aliyun.com/nexus/content/repositories/jcenter' }
  maven { url 'http://maven.aliyun.com/nexus/content/repositories/google' }
  mavenCentral()
}

dependencies {
  {% for d in dependencies -%}
  {{ d.to_gradle_line() }}
  {% endfor %}
}

test {
  useJUnitPlatform()
}
"""

APP_KT = """
package {{package}}
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
open class App

fun main(args: Array<String>) {
  runApplication<App>(*args)
}
"""

APP_TESTS_KT = """
package {{package}}
import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
class AppTests {
  @Test
  fun contextLoads() {
  }
}
"""


class Dependency:
    def __init__(self, group, artifact, version='', scope='implementation'):
        self.scope = scope
        self.group = group
        self.artifact = artifact
        self.version = version
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Dependency):
            return False
        return self.scope == other.scope and self.group == other.group and \
            self.artifact == other.artifact and self.version == other.version

    def to_gradle_line(self):
        version_suffix = f':{self.version}' if self.version else ''
        return f"{self.scope} '{self.group}:{self.artifact}{version_suffix}'"


# init gradle project for kotlin

def init_project(k, dependencies):
    # get args
    args = k.get_args([
        k.option('--group', required=True, help="project group"),
        k.option('--artifact', required=True, help="project artifact"),
        k.option('--name', default='', help="project name [default=artifact]"),
        k.option('--desc', default='', help="project description"),
        k.option('--package', default='', help="package name [default=group.artifact]"),
        k.option('--jdk', default='1.8', help="jdk version", show_default=True),
        k.option('--sprintboot', 'springboot_version', default=default_springboot_version, help="springboot version", show_default=True),
        k.option('--kotlin', 'kotlin_version', default=default_kotlin_version, help="kotlin_vesion", show_default=True),
    ])
    if not args.name:
        args.name = args.artifact
    if not args.desc:
        args.desc = f"Project {args.name}"
    if not args.package:
        args.package = f'{args.group}.{args.artifact}'   
    args.package_dir = args.package.replace('.', '/')
    args.source_compatibility = args.jdk
    args.kotlin_jvm_target = args.jdk
    args.dependencies = dependencies or []
    args.dependencies = [
        Dependency('org.jetbrains.kotlin', 'kotlin-reflect'),
        Dependency('org.jetbrains.kotlin', 'kotlin-stdlib-jdk8'),
    ] + args.dependencies
    
    
    # Go
    k.write('README.md', README, args=args)
    k.write('.gitignore', k.curl_gitignore('Java'))
    k.write('settings.gradle', SETTINGS_GRADLE, args=args)
    k.write('build.gradle', BUILD_GRADLE, args=args)
    k.write(f'src/main/kotlin/{args.package_dir}/App.kt', APP_KT, args=args)
    k.mkdir(f'src/main/java')
    k.write('src/main/resources/application.properties', "")
    k.mkdir('src/main/resources/static')
    k.mkdir('src/main/resources/templates')
    k.write(f'src/test/kotlin/{args.package_dir}/AppTests.kt', APP_TESTS_KT, args=args)

    # return
    return args


    
