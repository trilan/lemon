desc "remove pyc's and pyo's from project directory"
task :clean do
  sh 'find . -name "*.py[co]" -delete'
end

desc "install Stylus, CoffeeScript and Handlebars node.js modules"
task :node_modules do
  sh 'npm install stylus'
  sh 'npm install coffee-script'
  sh 'npm install handlebars'
end
