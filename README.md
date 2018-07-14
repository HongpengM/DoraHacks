# PyMotionCorr
A python version of motion correction software tools for cyro - EM


# Hierarchy Structure


```python
PyMotionCorr / -------------------------------------Module
     cal_relative_offset.py
     docs.py
     read_and_cal_fft_gpu.py
     read_and_cal_offset.py
     test_import.py
    data/

    PyMotionCorr/          ---------------------------------Module
         align.py
         dim.py
         para.py
         pymo.py
        mrc/          --------------------------------------Module
             mrc.py
            this module serves for .mrc, .mrcs file reading and writing, along with display function        
            (**TODO**)
           * Refract this module for easy usage
           * Upgrade display function, which is writing .png files at present
             mrcViewer.py

        Core/          -------------------------------------Module
            Setup the require environment
             requirements.py

        utils/          ------------------------------------Module
             Utils function
             data.py
             display.py

        math/          -------------------------------------Module
             math.py
             this module include functions like cross-correlation, over determination systems solution etc used in motion correction
            (**TODO**) 
           * Add B factor low-pass filter to mrc image, which will solve **fixed-pattern noise** problem
           * point registration algorithm
           * Thon ring and cc_fit from CTFFIND
             register_translation_gpu.py


    test/          -----------------------------------------Module
         Unit Test module 
         (**TODO**) 
         * Run testall.py 
         testmath.py
         testmrc.py
         testpickle.py
         testregister_translation.py


```
