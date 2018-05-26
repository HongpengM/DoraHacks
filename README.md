# PyMotionCorr
A python version of motion correction software tools for cyro-EM



## Hierarchy Structure



```python
PyMotionCorr/             ------------------------Project

	PyMotionCorr/         ------------------------Module

		math/             ------------------------Submodule

			-- math.py 

			this module include functions like cross-	correlation, over determination systems solution etc used in motion correction

			(**TODO**) 
   * Add B factor low-pass filter to mrc image, which will solve **fixed-pattern noise** problem
   * motioncorr2 interpolation algorithm
   * point registration algorithm
   * Thon ring and cc_fit from CTFFIND

       Core/             ------------------------Submodule

       			--requirements.py
       	
       			(**TODO**) key environment requiremnets solving different version problem
       	
       			--process.py
       	
       			(**TODO**) this module will provide multi-process and multi-thread function
       	
       			--acceleration.py
       	
       			(**TODO**) this module will provide GPU acceleration computation using numba


       mrc/             ------------------------Submodule
       	
       			--mrc.py
       	    	this module serves for .mrc, .mrcs file reading and writing, along with display function       	
       			(**TODO**)
   * Refract this module for easy usage
   * Upgrade display function, which is writing .png files at present

	test/                ------------------------Testmodule
		--testmath.py
			unit test for PyMotionCorr math module
		--testmrc.py
			unit test for PyMotionCorr mrc module
		(**TODO**) Refract the test code

```
