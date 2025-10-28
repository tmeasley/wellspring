mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"info@wellspringmountain.org\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
\n\
" > ~/.streamlit/config.toml
