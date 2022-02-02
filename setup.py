#!/usr/bin/env python
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from setuptools import setup, Command

from distutils.command.build_py import build_py

with open('README.rst') as infile:
    long_description = infile.read()

from libname import __version__

setup(name='btnetauto_py',
      version=__version__,
      description='Simple library for automated report generating from the BTNet bug-tracker system',
      url='https://github.com/swifty94/btnetauto_py',
      license='Simplified BSD License',
      author='Kirill Rudenko',
      author_email='kirillrudenko1994@gmail.com',
      packages=['btnetauto_py'],
      provides=['btnetauto_py'],
      install_requires=['selenium==4.1.0', 'pandas==1.4.0'],
      cmdclass={'build_py': build_py},
      classifiers=[
                   "Programming Language :: Python",
                   "License :: OSI Approved :: BSD License",
                  ],
     )
