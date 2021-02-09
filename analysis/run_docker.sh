docker build -t data_master .

mkdir -p Data/Queries/q1 Data/Queries/q2 Data/Queries/q3 Data/Queries/q4 Data/Queries/q5
mkdir -p Results

docker run --rm -i -t \
    -v $(pwd)/Data/:/Data/ \
    data_master \
    /runMe.sh
