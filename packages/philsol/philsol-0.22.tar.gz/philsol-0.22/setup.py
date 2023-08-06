# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['philsol']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'scipy>=1.3,<2.0']

setup_kwargs = {
    'name': 'philsol',
    'version': '0.22',
    'description': 'A fully vectorial finite difference waveguide mode solver. Based on the algorithm of Zhu and Brown',
    'long_description': "# philsol\n## Modes for the Masses (Massless?)\nFed up with relying on expensive proprietary software for your electromagnetic waveguide research?  philsol might just be the package for you. \nThis is a fully vectorial finite difference waveguide mode solver. In a world where high performance hardware is cheaper than specialist software (including certain commercial packages which may or may not rhyme with my code), philsol throws elegence and sophistication out of the window and replaces it with brute force. \n\nThis is a direct Python implimentaion of the algorithm found in the paper: \n['Full-vectorial finite-difference analysis of microstructured optical fibres', by Zhu and Brown.](https://doi.org/10.1364/OE.10.000853)\n\nWarning: I haven't thoroughly tested so be wary and check the results are sensible...\n\nNew Warning: Original paper by Zhu and Brown is in gaussian not S. I. units. \nThis means that the constructed H fields must be corrected by a factor of $\\mu_0 c$ for calculations in S.I units. \n\n## Installation\n- Clone or download, and install with `python3 setup.py install` (you may need to install python-setuptools)\n- If you are new to python, the important bit is the function in core.py which can be run by itself. \n\n## Examples\n- Commented example projects can be found in the *examples* directory.\n- To run the examples, first install philsol to your Python environment (see above)\n\n## Features\n### Solver\n- Solves vector Maxwell(Helmholtz) equations in 2D for arbitary refractive index profile.\n- Return x and y componants of electric field.\n- philsol can handle anisotropic refractive indices with diagonal tensor.\n- Currently hard coded with conductive boundary.\n- Now includes choice of eigensolver: the default scipy.sparse solver based on ARPACK and Petsc (but you will need a working install of slepc4py and petsc4py)\n- Extra field componants Ez, Hx, Hy, Hz can be calculated from construct module\n- Periodic boundary conditions \n\n### Geometry building\n- The quickest way of importing geometry is with a bitmap image \n- See *examples/example_image.py* for an example in loading .bpm images\n- See *examples/example_build.py* for an example in building geometry using PIL/Pillow\n\n## To do \n- More intelligent geometry aproximation (e.g pixel interpolation on curved boundaries)\n- More boundry condition options Bloch, PML...\n- GPU eigensolving\n\n\n",
    'author': 'Phil Main',
    'author_email': 'philmain28@gmail.com',
    'url': 'https://github.com/philmain28/philsol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
