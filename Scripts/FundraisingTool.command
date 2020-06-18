#!/bin/bash

echo ""
echo "- - - - - - - - - -"
echo "*** HOW TO USE ***"
echo ""
echo -e "\"Type-A node\": The first node-type in your 2-mode network (e.g. LP)."
echo -e "\"Type-B node\": The second node-type in your 2-mode network (e.g. VC)."
echo -e "\"Input folder\": The absolute path of the folder that contains all input .csv files."
echo -e "\"Output folder\": The absolute path of the folder that you'd like to save the output .csv files."
echo -e "(NOTE: Each argument should NOT contain any SPACES.)"
echo "- - - - - - - - - -"
echo ""

read -p "Type-A node: " typeAnode
if [ -z "$typeAnode" ]
then
  echo "ERROR: No input detected."
  echo ""
  exit 1
fi

read -p "Type-B node: " typeBnode
if [ -z "$typeBnode" ]
then
  echo "ERROR: No input detected."
  echo ""
  exit 1
fi

read -p "Input folder: " indir
if [ -z "$indir" ]
then
  echo "ERROR: No input detected."
  echo ""
  exit 1
elif [ ! -d "$indir" ]
then
  echo "ERROR: Directory $indir DOES NOT EXIST."
  echo ""
  exit 1
fi

read -p "Output folder: " outdir
if [ -z "$outdir" ]
then
  echo "ERROR: No input detected."
  echo ""
  exit 1
elif [ ! -d "$outdir" ]
then
  echo "ERROR: Directory $outdir DOES NOT EXIST."
  echo ""
  exit 1
fi

# ----------

# Activate virtual environment
source /Users/cleonwong/Desktop/Code/python-virtual-environments/Venture-Capital-Fundraising-Tool_env/bin/activate

# Begin script if all arguments are correct.
CWD="${0%/*}" # This gets current working directory
outdirGraph="$outdir/Graphs"

# List of output files names. Note that file names are absolute paths:
combinedOUT="$outdir/combined$typeAnode"
nodesOUT="$outdir/"$typeAnode"nodes"
nodesTaggedOUT="$outdir/"$typeAnode"nodesTagged"
edges2modeOUT="$outdir/"$typeAnode"edges2mode"
edges1modeOUT="$outdir/"$typeAnode"edges1mode"
nodesCentrality2modeOUT="$outdir/"$typeAnode"nodesCentrality2mode"
nodesCentrality1modeOUT="$outdir/"$typeAnode"nodesCentrality1mode"
target2modeOUT="$outdir/target$typeAnode""2mode"
target1modeOUT="$outdir/target$typeAnode""1mode"
compared2modeOUT="$outdir/compared$typeAnode""2mode"
compared1modeOUT="$outdir/compared$typeAnode""1mode"
graph1modeOUT="$outdirGraph/graph1mode"
graph2modeOUT="$outdirGraph/graph2mode"

export PYTHON_VERSION3=`python3 -c 'import sys; version=sys.version_info[:3]; print(version[0])'`
export PYTHON_VERSION2=`python -c 'import sys; version=sys.version_info[:3]; print(version[0])'`

if [ "$PYTHON_VERSION3"=="3" ]
then
  # For 2-mode outputs:
  echo -ne '\n'
  python3 $CWD/combined.py $indir $combinedOUT
  echo -ne 'PROGRESS: -------------------- (0% | combined.py)\r'
  python3 $CWD/nodes.py $combinedOUT $nodesOUT
  echo -ne '\033[KPROGRESS: ##------------------ (10% | nodes.py)\r'
  python3 $CWD/nodesTagged.py $nodesOUT $nodesTaggedOUT
  echo -ne '\033[KPROGRESS: ####---------------- (20% | nodesTagged.py)\r'
  python3 $CWD/edges2mode.py $combinedOUT $edges2modeOUT
  echo -ne '\033[KPROGRESS: ######-------------- (30% | edges2mode.py)\r'
  python3 $CWD/nodesCentrality2mode.py $edges2modeOUT $nodesOUT $nodesCentrality2modeOUT
  echo -ne '\033[KPROGRESS: ########------------ (40% | nodesCentrality2mode.py)\r'
  python3 $CWD/target2mode.py $nodesCentrality2modeOUT $target2modeOUT
  echo -ne '\033[KPROGRESS: ##########---------- (50% | target2mode.py)\r'
  mkdir -m 777 $outdirGraph
  python3 $CWD/graph2mode.py $edges2modeOUT $nodesTaggedOUT $graph2modeOUT $typeBnode
  echo -ne '\033[KPROGRESS: ############-------- (60% | graph2mode.py)\r'

  # For 1-mode outputs:
  python3 $CWD/edges1mode.py $edges2modeOUT $edges1modeOUT
  echo -ne '\033[KPROGRESS: ##############------ (70% | edges1mode.py)\r'
  python3 $CWD/nodesCentrality1mode.py $edges1modeOUT $nodesOUT $nodesCentrality1modeOUT
  echo -ne '\033[KPROGRESS: ################---- (80% | nodesCentrality1mode.py)\r'
  python3 $CWD/target1mode.py $nodesCentrality1modeOUT $target1modeOUT
  echo -ne '\033[KPROGRESS: ##################-- (90% | target1mode.py)\r'
  python3 $CWD/graph1mode.py $edges1modeOUT $nodesTaggedOUT $graph1modeOUT
  echo -ne '\033[KPROGRESS: #################### (100% | graph1mode.py)'
  echo -ne '\n'
  echo -ne '\n'

elif [ "$PYTHON_VERSION2"=="2" ]
then
  # For 2-mode outputs:
  echo -ne '\n'
  python $CWD/combined.py $indir $combinedOUT
  echo -ne 'PROGRESS: -------------------- (0% | combined.py)\r'
  python $CWD/nodes.py $combinedOUT $nodesOUT
  echo -ne '\033[KPROGRESS: ##------------------ (10% | nodes.py)\r'
  python $CWD/nodesTagged.py $nodesOUT $nodesTaggedOUT
  echo -ne '\033[KPROGRESS: ####---------------- (20% | nodesTagged.py)\r'
  python $CWD/edges2mode.py $combinedOUT $edges2modeOUT
  echo -ne '\033[KPROGRESS: ######-------------- (30% | edges2mode.py)\r'
  python $CWD/nodesCentrality2mode.py $edges2modeOUT $nodesOUT $nodesCentrality2modeOUT
  echo -ne '\033[KPROGRESS: ########------------ (40% | nodesCentrality2mode.py)\r'
  python $CWD/target2mode.py $nodesCentrality2modeOUT $target2modeOUT
  echo -ne '\033[KPROGRESS: ##########---------- (50% | target2mode.py)\r'
  mkdir -m 777 $outdirGraph
  python $CWD/graph2mode.py $edges2modeOUT $nodesTaggedOUT $graph2modeOUT $typeBnode
  echo -ne '\033[KPROGRESS: ############-------- (60% | graph2mode.py)\r'

  # For 1-mode outputs:
  python $CWD/edges1mode.py $edges2modeOUT $edges1modeOUT
  echo -ne '\033[KPROGRESS: ##############------ (70% | edges1mode.py)\r'
  python $CWD/nodesCentrality1mode.py $edges1modeOUT $nodesOUT $nodesCentrality1modeOUT
  echo -ne '\033[KPROGRESS: ################---- (80% | nodesCentrality1mode.py)\r'
  python $CWD/target1mode.py $nodesCentrality1modeOUT $target1modeOUT
  echo -ne '\033[KPROGRESS: ##################-- (90% | target1mode.py)\r'
  python $CWD/graph1mode.py $edges1modeOUT $nodesTaggedOUT $graph1modeOUT
  echo -ne '\033[KPROGRESS: #################### (100% | graph1mode.py)'
  echo -ne '\n'
  echo -ne '\n'

else
  echo "ERROR: No Python detected."
fi
