echo "installing the 'robo' and 'generateSalt' commands..."
sudo cp src/Robocrypt.py /usr/local/bin/robo
sudo cp src/generateSalt.py /usr/local/bin/generateSalt
sudo chmod 744 /usr/local/bin/robo
sudo chmod 744 /usr/local/bin/generateSalt
echo "installation completed successfully."