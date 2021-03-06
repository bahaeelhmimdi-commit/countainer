from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe 
from pythonforandroid.recipe import sh
from os.path import join
from multiprocessing import cpu_count
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory
class DlibRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'dlib'
    version = '19.17'
    url = 'http://dlib.net/files/dlib-{version}.zip'
    depends = ['op','numpy']
    call_hostpython_via_targetpython = False
    def get_lib_dir(self, arch):
        return join(self.get_build_dir(arch.arch), 'build', 'lib', arch.arch)
    def get_recipe_env(self, arch):
        env = super(DlibRecipe, self).get_recipe_env(arch)
        env['ANDROID_NDK'] = self.ctx.ndk_dir 
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        return env
    def build_arch(self, arch):
        build_dir = join(self.get_build_dir(arch.arch), 'build')
        shprint(sh.mkdir, '-p', build_dir)
        with current_directory(build_dir):
            env = self.get_recipe_env(arch)
            python_major = self.ctx.python_recipe.version[0]
            python_include_root = self.ctx.python_recipe.include_root(arch.arch)
            python_site_packages = self.ctx.get_site_packages_dir()
            python_link_root = self.ctx.python_recipe.link_root(arch.arch)
            python_link_version = self.ctx.python_recipe.major_minor_version_string
            if 'python3' in self.ctx.python_recipe.name:
             python_link_version += 'm'
            python_library = join(python_link_root, 'libpython{}.so'.format(python_link_version))
            python_include_numpy = join(python_site_packages, 'numpy', 'core', 'include')
            python_include_opencv = join(python_site_packages, 'op', 'core', 'include')
            shprint(sh.cmake, '-DP4A=ON', '-DANDROID_ABI={}'.format(arch.arch), '-DANDROID_STANDALONE_TOOLCHAIN={}'.format(self.ctx.ndk_dir), '-DANDROID_NATIVE_API_LEVEL={}'.format(self.ctx.ndk_api), '-DANDROID_EXECUTABLE={}/tools/android'.format(env['ANDROID_SDK']), '-DCMAKE_TOOLCHAIN_FILE={}'.format( join(self.ctx.ndk_dir, 'build', 'cmake', 'android.toolchain.cmake')), '-DCMAKE_SHARED_LINKER_FLAGS=-L{path} -lpython{version}'.format( path=python_link_root, version=python_link_version), '-DBUILD_WITH_STANDALONE_TOOLCHAIN=ON', '-DBUILD_SHARED_LIBS=OFF', '-DBUILD_STATIC_LIBS=ON', '-DBUILD_dlib_java=OFF', '-DBUILD_dlib_java_bindings_generator=OFF',  '-DBUILD_dlib_highgui=OFF',  '-DBUILD_dlib_imgproc=OFF',  '-DBUILD_dlib_flann=OFF', '-DBUILD_TESTS=OFF', '-DBUILD_PERF_TESTS=OFF', '-DENABLE_TESTING=OFF', '-DBUILD_EXAMPLES=OFF', '-DBUILD_ANDROID_EXAMPLES=OFF', '-DBUILD_DLIB_PYTHON{major}=ON'.format(major=python_major), '-DBUILD_DLIB_PYTHON{major}=OFF'.format( major='2' if python_major == '3' else '3'), '-DDLIB_SKIP_PYTHON_LOADER=OFF', '-DDLIB_PYTHON{major}_INSTALL_PATH={site_packages}'.format( major=python_major, site_packages=python_site_packages), '-DPYTHON_DEFAULT_EXECUTABLE={}'.format(self.ctx.hostpython), '-DPYTHON{major}_EXECUTABLE={host_python}'.format( major=python_major, host_python=self.ctx.hostpython), '-DPYTHON{major}_INCLUDE_PATH={include_path}'.format( major=python_major, include_path=python_include_root), '-DPYTHON{major}_LIBRARIES={python_lib}'.format( major=python_major, python_lib=python_library), '-DPYTHON{major}_NUMPY_INCLUDE_DIRS={numpy_include}'.format( major=python_major, numpy_include=python_include_numpy), '-DPYTHON{major}_PACKAGES_PATH={site_packages}'.format( major=python_major, site_packages=python_site_packages), self.get_build_dir(arch.arch), _env=env)
            shprint(sh.cmake, '-DCOMPONENT=python', '-P', './cmake_install.cmake') 
            sh.cp('-a', sh.glob('./lib/{}/lib*.so'.format(arch.arch)), self.ctx.get_libs_dir(arch.arch))
recipe = DlibRecipe()