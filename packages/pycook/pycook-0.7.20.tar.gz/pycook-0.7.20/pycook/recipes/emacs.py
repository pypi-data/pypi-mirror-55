#* Imports
import pycook.elisp as el
lf = el.lf

#* Functions
def elisp_files_cwd():
    return el.directory_files(el.default_directory(), False, ".*el$")

#* Recipes
def install(recipe, *packages):
    packages_str = " ".join(packages)
    return el.emacs_batch_eval(lf("(cook-install-deps '({packages_str}))"))

def compile(recipe, *fnames):
    fnames = fnames or elisp_files_cwd()
    fnames_str = " ".join(['"' + fname + '"' for fname in fnames])
    return el.emacs_batch_eval(lf("(cook-byte-compile {fnames_str})"))

def elpa(recipe, *fnames):
    """Start Emacs, load elpa.el, and FNAMES."""
    fnames = fnames or elisp_files_cwd()
    fnames = ["/usr/local/cook/elpa.el", *fnames]
    fnames_str = " ".join(['-l "' + fname + '"' for fname in fnames])
    return [
        "emacs --version",
        lf("emacs -Q {fnames_str}")
    ]
