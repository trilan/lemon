STATIC_ROOT = 'lemon/extradmin/static/extradmin'
JOINED_CSS_PREREQUISITES = [
  'reset.css', 'default.css', 'base.css', 'jquery.ui.css',
  'changelist.css', 'changeform.css', 'jquery.datetimepicker.css'
].map { |name| "#{STATIC_ROOT}/css/#{name}" }

desc "remove pyc's and pyo's from project directory"
task :clean do
  sh 'find . -name "*.py[co]" -delete'
end

task :build_css => [
  "#{STATIC_ROOT}/css/compressed.css",
  "#{STATIC_ROOT}/css/auth_permissions.css",
]

file "#{STATIC_ROOT}/css/compressed.css" => JOINED_CSS_PREREQUISITES do |t|
  sh "cat #{t.prerequisites.join(' ')} | yuicompressor --type css > #{t.name}"
end

%w(default base changeform changelist auth_permissions).each do |name|
  file "#{STATIC_ROOT}/css/#{name}.css" => "#{STATIC_ROOT}/stylus/#{name}.styl" do |t|
    sh "bin/compile_css #{t.prerequisites.first} #{t.name}"
  end
end
