#!/usr/bin/env ruby

require File.join([File.dirname(__FILE__), '/../../spec_helper'])

describe "util test" do

  before(:all) do
    @agent = MCollective::Test::LocalAgentTest.new("example", :config => {:libdir => "../../../../"}).plugin
  end

  describe "#check_file_exist" do
     it "should have valid metadata" do
       @agent.expects(:run).returns(0)
       result = @agent.call(:check_file_exist, {:path => "/tmp/file.txt"})
       result.should be_successful
       expect(result).to eq({:data=>{:retcode=>0}, :statusmsg=>"OK", :statuscode=>0})
     end
  end
end
