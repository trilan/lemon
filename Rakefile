task :default => [:clean, :compile_css]

desc "remove pyc's and pyo's from project directory"
task :clean do
  sh 'find . -name "*.py[co]" -delete'
end

desc "compile stylus to css"
task :compile_css do
  sh 'bin/compile_css'
end
