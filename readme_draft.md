# PyMotionCorr
A python version of motion correction software tools for cyro-EM

## Hierarchy Structure
```python
PyMotionCorr/          -------------------------------------Module
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
             mrcViewer.py

        Core/          -------------------------------------Module
             requirements.py

        utils/          ------------------------------------Module
             data.py
             display.py

        math/          -------------------------------------Module
             math.py
             register_translation_gpu.py


    test/          -----------------------------------------Module
         testmath.py
         testmrc.py
         testpickle.py
         testregister_translation.py


```