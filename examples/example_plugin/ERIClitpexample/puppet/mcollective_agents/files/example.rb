require 'open3'
def get_system_path
    res = %x[source /etc/profile;  facter | grep path]
    path =  res.split("=>").last
    return path
end       

def log(message)
# $0 is the current script name
  Syslog.open($0, Syslog::LOG_PID | Syslog::LOG_CONS) { |s| s.err message }
  end

 
module MCollective
  module Agent
    class Example<RPC::Agent
      #this is the method called from the callback task via the callbackapi.      
      action "check_file_exist" do
        #path is passed in from the callback_api.rpc_command within the plugin
        path = request[:path]
        
        # An example of the cmd would be "ls -l /tmp/test.conf.
        # The cmd will return the file or an error    
        cmd = %{ls -l } + path
        reply[:retcode] = run("#{cmd}",
                             :stdout => :out,
                             :stderr => :err,
                             :chomp => true,
                             :environment => {"PATH" => get_system_path})
      end
    end
  end
end
