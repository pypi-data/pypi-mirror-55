import pycondor
import os


class Dag(object):
    """Base Dag object to handle the creation of the DAG

    Parameters
    ----------
    inputs: varaha.inputs.Inputs
        object containing the command line arguments 
    """
    def __init__(self, inputs):
        self.inputs = inputs
        string = "%s/{}" % (inputs.outdir)
        self.error = string.format("error")
        self.log = string.format("log")
        self.output = string.format("output")
        self.submit = string.format("submit")
        self.dagman = pycondor.Dagman(name="varaha", submit=self.submit)

    @property
    def bash_file(self):
        return os.path.join(self.submit, "varaha.sh")

    @property
    def output_directories(self):
        dirs = {
            "error": self.error, "log": self.log, "output": self.output,
            "submit": self.submit
        }
        return dirs

    def build(self):
        """Build the pycondor dag
        """
        self.dagman.build()
        self.write_bash_script()
        print("Dag Generation complete. To submit jobs run:\n")
        print("$ condor_submit_dag {}".format(self.dagman.submit_file))

    def build_submit(self):
        """Submit the pycondor dag
        """
        self.dagman.build_submit()

    def write_bash_script(self):
        """Write a bash script containing all of the command lines used
        """
        with open(self.bash_file, "w") as f:
            f.write("#!/usr/bin/env bash\n\n")
            for node in self.dagman.nodes:
                f.write("# {}\n".format(node.name))
                f.write(
                    "# PARENTS {}\n".format(
                        " ".join([job.name for job in node.parents])
                    )
                )
                f.write(
                    "# CHILDREN {}\n".format(
                        " ".join([job.name for job in node.children])
                    )
                )
                job_str = "{} {}\n\n".format(node.executable, node.args[0].arg)
                job_str = job_str.replace("$(Cluster)", "0")
                job_str = job_str.replace("$(Process)", "0")
                f.write(job_str)


class Node(object):
    """Base node object to handle condor job creation

    Parameters
    ----------
    inputs: varaha.inputs.Inputs
        object containing the command line arguments
    name: str
        the name of the job
    """
    def __init__(self, inputs, job_name, output_directories, dagman):
        self.inputs = inputs
        self.job_name = job_name
        self.output_directories = output_directories
        self.dagman = dagman
        self._executable = self.get_executable("varaha_pipe")

    @staticmethod
    def get_executable(executable):
        """Find the path to the executable

        Parameters
        ----------
        executable: str
            the name of the executable you wish to find
        """
        from distutils.spawn import find_executable

        return find_executable(executable)

    @property
    def output_directories(self):
        return self._output_directories

    @output_directories.setter
    def output_directories(self, output_directories):
        self._output_directories = output_directories
        for key, item in output_directories.items():
            setattr(self, key, item)

    @property
    def executable(self):
        return self._executable

    @property
    def request_memory(self):
        return "8 GB"

    @property
    def request_disk(self):
        return None

    @property
    def request_cpus(self):
        return 1

    @property
    def getenv(self):
        return True

    @property
    def universe(self):
        return "vanilla"

    @property
    def extra_lines(self):
        return "accounting_group = {}".format(self.inputs.accounting_group)

    def add_parent(self, parent):
        """Add a parent to the node

        Parameters
        ----------
        parent: 
            
        """
        self.job.add_parent(parent)

    def add_child(self, child):
        """Add a child to the node

        Parameters
        ----------
        child: varaha.condor.Node
            child node you wish to add to your job
        """
        self.job.add_child(child)

    def create_pycondor_job(self):
        self.job = pycondor.Job(
            name=self.job_name, executable=self.executable, submit=self.submit,
            error=self.error, log=self.log, output=self.output,
            request_memory=self.request_memory, request_disk=self.request_disk,
            request_cpus=self.request_cpus, getenv=self.getenv,
            universe=self.universe, extra_lines=self.extra_lines,
            dag=self.dagman, arguments=self.arguments
        )


class DataFindNode(Node):
    """Object to handle the creation of a datafind job

    Parameters
    ----------
    inputs: varaha.inputs.Inputs
        object containing the command line arguments
    """
    def __init__(self, inputs, output_directories, dagman):
        super(DataFindNode, self).__init__(
            inputs, "data_find", output_directories, dagman
        )
        self.create_pycondor_job()

    @property
    def universe(self):
        return "local"

    @property
    def arguments(self):
        arguments = [
            "--gid", self.inputs.gid, "--outdir", self.output, "--grab_data"
        ]
        return " ".join(arguments)


class VarahaNode(Node):
    """Object to handle the creation of the main varaha job

    Parameters
    ----------
    inputs: varaha.inputs.Inputs
        object containing the command line arguments
    """
    def __init__(self, inputs, opts, output_directories, dagman):
        super(VarahaNode, self).__init__(inputs, "sampler", output_directories, dagman)
        self.opts = opts
        self.create_pycondor_job()

    @property
    def request_cpus(self):
        return self.inputs.nparallel

    @property
    def arguments(self):
        arguments = []
        obj = self.opts
        ignore_keys = [
            "condor_submit", "accounting_group", "accounting_group_user", "grab_data",
            "varaha", "condor"
        ]
        for key, item in vars(obj).items():
            if isinstance(item, dict) or item is None:
                pass
            elif key in ignore_keys:
                pass
            else:
                arguments.append("--{}".format(key))
                arguments.append("{}".format(item))
        return " ".join(arguments)


class PESummaryNode(Node):
    """Object to handle the creation of the PESummary job

    Parameters
    ----------
    inputs: varaha.inputs.Inputs
        object containing the command line arguments
    """
    def __init__(self, inputs, output_directories, dagman):
        super(PESummaryNode, self).__init__(
            inputs, "pesummary", output_directories, dagman
        )
        self.create_pycondor_job()

    @property
    def request_cpus(self):
        return 2

    @property
    def executable(self):
        return self.get_executable("summarypages")

    @property
    def arguments(self):
        arguments = [
            "--webdir", self.inputs.webdir, "--gw", "--approximant", "IMRPhenomD",
            "--gracedb", self.inputs.gid, "--samples",
            os.path.join(self.output, "posterior_samples.dat"),
            "--config", self.inputs.ini
        ]
        return " ".join(arguments)
