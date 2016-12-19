cd /apps/waq/backend/dse/
sudo mkdir -p /usr/lib/jvm
sudo tar zxvf jdk-8u101-linux-x64.tar.gz -C /usr/lib/jvm
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_101/bin/java" 1
sudo update-alternatives --config java
java -version
echo "deb https://ankittharwani%40gmail.com:PDJ1120a@debian.datastax.com/enterprise stable main" | sudo tee -a /etc/apt/sources.list.d/datastax.sources.list
curl -L https://debian.datastax.com/debian/repo_key | sudo apt-key add -
sudo apt-get update


sudo apt-get install python3-setuptools
sudo easy_install3 pip
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install numpy
pip3 install sklearn
pip3 install flask
pip3 install dill
pip3 install scipy
pip3 install pandas
pip3 install flask_restful
pip3 install scikit-learn==0.17.1


sudo apt-get install nodejs
sudo apt-get install npm
