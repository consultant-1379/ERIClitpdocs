#  Puppet Manifest file for example plugin
define test_example::test_example(
  $filename,
  $file_ensure
)
{

  file {"/tmp/${filename}":
    ensure => $file_ensure,
    owner  => nobody,
    group  => nobody,
  }
}
