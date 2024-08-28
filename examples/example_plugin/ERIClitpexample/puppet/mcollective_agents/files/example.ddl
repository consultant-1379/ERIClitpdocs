metadata    :name        => "example",
            :description => "API for an example cli commands",
            :author      => "User < User@ericsson.com>",
            :license     => "Ericsson",
            :version     => "1.0",
            :url         => "http://ericsson.com",
            :timeout     => 10
 
action "check_file_exist", :description => "Checks if a file has been created in a directory" do
    display :always
 
    input  :path,
           :prompt      => "Path",
           :description => "The path to be checked",
           :type        => :string,
           :validation  => '^((?:[a-zA-Z]\:){0,1}(?:[\\/][\w.-]+){1,})$',
           :optional    => false,
           :maxlength   => 100
 
    output :retcode,
           :description => "The exit code from running the command",
           :display_as => "Result code"
    output :out,
           :description => "The stdout from running the command",
           :display_as => "out"
    output :err,
           :description => "The stderr from running the command",
           :display_as => "err"
end
