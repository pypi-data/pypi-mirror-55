from .base import Dataset
from .utils import extract_tar
from .utils import URL

class PackagedDataset(Dataset):
    """Packaged Dataset in .tar.* foramt.

    Args:
        path (str): Root directory where ``dataset_name/samples.npy`
            and ``dataset_name/targets.npy`` exists.
        download (bool, optional): If True, downloads the dataset from internet
            and puts it in root directory. If dataset is already downloaded, it
            will not be downloaded again.
        sample_transform (callable, optional): A function/transform that takes
            a sample and returns a transformed version.
        target_transform (callable, optional): A function/transform that takes
            a target and transform it.

    """

    url = ''

    def __init__(self, download=False, **kwargs):
        # verify download flag
        if not isinstance(download, bool):
            raise ValueError("`download` needs to be True or False.")

        # verify if dataset is ready
        try:
            super().__init__(**kwargs)
        except ValueError:
            if download:
                url = URL(self.url)
                # download compressed file from source if not exists
                fpath = self.root / url.url_filename
                if not fpath.is_file():
                    url.download(self.root)
                # extract file under root directory
                print("Extracting dataset (this may take minutes to hours) ...")
                extract_tar(fpath, self.root)
                # try initiate DatasetArrayFolder again
                super().__init__(**kwargs)
            else:
                raise ValueError(f"{self.root} contains no valid dataset. "
                                 f"Consider set `download=True` and remove broken bz2 file.")


class Wenchuan(PackagedDataset):
    """`Wenchuan <https://arxiv.org/abs/1901.06396>`_ Dataset.

    Args:
        path (str): Root directory where ``wenchuan/samples.npy`
            and ``wenchuan/targets.npy`` exists.
        download (bool, optional): If True, downloads the dataset from internet
            and puts it in root directory. If dataset is already downloaded, it
            will not be downloaded again.
        sample_transform (callable, optional): A function/transform that takes
            a sample and returns a transformed version.
        target_transform (callable, optional): A function/transform that takes
            a target and transform it.

    """

    url = 'https://www.dropbox.com/s/idk4eyyleodof2q/wenchuan.tar?dl=1'


class Mariana(PackagedDataset):
    """`Mariana <https://arxiv.org/abs/1901.06396>`_ Dataset.

    Args:
        path (str): Root directory where ``mariana/samples.npy`
            and ``mariana/targets.npy`` exists.
        download (bool, optional): If True, downloads the dataset from internet
            and puts it in root directory. If dataset is already downloaded, it
            will not be downloaded again.
        sample_transform (callable, optional): A function/transform that takes
            a sample and returns a transformed version.
        target_transform (callable, optional): A function/transform that takes
            a target and transform it.

    """

    url = 'https://www.dropbox.com/s/2hpurxeoo2ungim/mariana.tar?dl=1'


class SCSN(PackagedDataset):
    """`SCSN <https://service.scedc.caltech.edu/ftp/ross_etal_2018_bssa/scsn_ps_2000_2017_shuf.hdf5>`_ Dataset.

    Args:
        path (str): Root directory where ``scsn/samples.npy`
            and ``scsn/targets.npy`` exists.
        download (bool, optional): If True, downloads the dataset from internet
            and puts it in root directory. If dataset is already downloaded, it
            will not be downloaded again.
        sample_transform (callable, optional): A function/transform that takes
            a sample and returns a transformed version.
        target_transform (callable, optional): A function/transform that takes
            a target and transform it.

    """

    url = 'https://www.dropbox.com/s/u16lkjxliw8fouj/scsn.tar?dl=1'
