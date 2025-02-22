FROM python:3.12.7

# Update the package list
RUN apt-get update

# Define the installation path as an environment variable
ENV INSTALL_PATH /faq_chat

# Add the installation path to the Python path
ENV PYTHONPATH="${INSTALL_PATH}:${PYTHONPATH}"

# Create the working directory
RUN mkdir -p $INSTALL_PATH

# Set the working directory
WORKDIR $INSTALL_PATH

# Copy the requirements file
COPY requirements.txt requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U langchain-community

# Copy the project files to the container
COPY . .

# Grant execute permissions to the entrypoint script
RUN chmod +x entrypoint.sh

# Define the entrypoint
ENTRYPOINT [ "./entrypoint.sh" ]
