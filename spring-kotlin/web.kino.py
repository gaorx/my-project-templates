

HELLO_CONTROLLER_KT = """
package {{package}}.controller
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.RequestMapping

@RestController
class HelloController {
    @RequestMapping("/")
    fun index(): String = "Hello SprintBoot"
}
"""

def main(k):
    common = k.import_('common.py')
    d = common.Dependency
    args = common.init_project(k, [
        d('org.springframework.boot', 'spring-boot-starter-web'),
        d('com.fasterxml.jackson.module', 'jackson-module-kotlin'),
        d('org.springframework', 'spring-jdbc'),
        d('mysql', 'mysql-connector-java'),
        d('org.springframework.boot', 'spring-boot-starter-test', scope='testImplementation'),
    ])
    k.write(f'src/main/kotlin/{args.package_dir}/controller/HelloController.kt', HELLO_CONTROLLER_KT, args=args)
    k.mkdir(f'src/main/kotlin/{args.package_dir}/repository')
    k.mkdir(f'src/main/kotlin/{args.package_dir}/service')
    k.mkdir(f'src/main/kotlin/{args.package_dir}/util')
