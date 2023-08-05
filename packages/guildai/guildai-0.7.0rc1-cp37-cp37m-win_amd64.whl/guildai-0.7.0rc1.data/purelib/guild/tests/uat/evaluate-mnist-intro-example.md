# Evaluate MNIST intro example

Once an `mnist-intro` model is trained, we can run the `evaluate`
operation to test it against all of the test data.

    >>> cd("examples/mnist")
    >>> run("guild run intro:evaluate -y --no-gpus")
    Masking available GPUs (CUDA_VISIBLE_DEVICES='')
    Resolving data dependency...
    Resolving train dependency
    Using output from run ...
    INFO: [tensorflow] Restoring parameters from ./model/export...
    Test accuracy=0...
    <exit 0>
