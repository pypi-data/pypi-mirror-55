# -*- coding: utf-8 -*-

import re


FDS_MANUAL_CHAPTER_LIST_OF_INPUT_PARAMETERS = r"""

\chapter{Alphabetical List of Input Parameters}

This appendix lists all of the input parameters for FDS in separate tables grouped by namelist, these tables are in alphabetical order along with the parameters within them. This is intended to be used as a quick reference and does not replace reading the detailed description of the parameters in the main body of this guide. See Table \ref{tbl:namelistgroups} for a cross-reference of relevant sections and the tables in this appendix. The reason for this statement is that many of the listed parameters are mutually exclusive -- specifying more than one can cause the program to either fail or run in an unpredictable manner. Also, some of the parameters trigger the code to work in a certain mode when specified. For example, specifying the thermal conductivity of a solid surface triggers the code to assume the material to be thermally-thick, mandating that other
properties be specified as well. Simply prescribing as many properties as possible from a handbook is bad practice. Only prescribe those parameters which are necessary to describe the desired scenario. Note that you may use the character string {\ct FYI} on any namelist line to make a note or comment.




\section{\texorpdfstring{{\tt BNDF}}{BNDF} (Boundary File Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Boundary file parameters ({\ct BNDF} namelist group)]{For more information see Section~\ref{info:BNDF}.}
\label{tbl:BNDF} \\
\hline
\multicolumn{5}{|c|}{{\ct BNDF} (Boundary File Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct BNDF} (Boundary File Parameters)} \\
\hline \hline
\endhead
{\ct CELL\_CENTERED}             & Logical     & Section \ref{info:BNDF}                 &           & {\ct .FALSE.}   \\ \hline
{\ct MATL\_ID}                   & Character   & Section \ref{info:outputquantities}     &           &                 \\ \hline
{\ct PART\_ID}                   & Character   & Section \ref{info:outputquantities}     &           &                 \\ \hline
{\ct PROP\_ID}                   & Character   & Section \ref{info:BNDF}                 &           &                 \\ \hline
{\ct QUANTITY}                   & Character   & Section \ref{info:outputquantities}     &           &                 \\ \hline
{\ct SPEC\_ID}                   & Character   & Section \ref{info:outputquantities}     &           &                 \\ \hline
{\ct TEMPORAL\_STATISTIC}        & Character   & Section \ref{info:BNDF}                 &           &                 \\ \hline
\end{longtable}


\vspace{\baselineskip}

\section{\texorpdfstring{{\tt CATF}}{CATF} (Concatenate Input Files Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Concatenate Input Files parameters ({\ct CATF} namelist group)]{For more information see Section~\ref{info:CATF}.}
\label{tbl:CATF} \\
\hline
\multicolumn{5}{|c|}{{\ct CATF} (Concatenate Input Files Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct CATF} (Concatenate Input Files Parameters)} \\
\hline \hline
\endhead
{\ct OTHER\_FILES}    & Character Array  & Section \ref{info:CATF}                 &           &   \\ \hline
\end{longtable}

\vspace{\baselineskip}

\section{\texorpdfstring{{\tt CLIP}}{CLIP} (Clipping Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Clipping parameters ({\ct CLIP} namelist group)]{For more information see Section~\ref{info:CLIP}.}
\label{tbl:CLIP} \\
\hline
\multicolumn{5}{|c|}{{\ct CLIP} (Specified Upper and Lower Limits)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct CLIP} (Specified Upper and Lower Limits)} \\
\hline \hline
\endhead
{\ct MAXIMUM\_DENSITY}              & Real           & Section~\ref{info:CLIP}      & kg/m$^3$   &     \\ \hline
{\ct MAXIMUM\_TEMPERATURE}          & Real           & Section~\ref{info:CLIP}      & $^\circ$C  &     \\ \hline
{\ct MINIMUM\_DENSITY}              & Real           & Section~\ref{info:CLIP}      & kg/m$^3$   &     \\ \hline
{\ct MINIMUM\_TEMPERATURE}          & Real           & Section~\ref{info:CLIP}      & $^\circ$C  &     \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt COMB}}{COMB} (General Combustion Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[General combustion parameters ({\ct COMB} namelist group)]{For more information see Chapter~\ref{info:COMB}.}
\label{tbl:COMB} \\
\hline
\multicolumn{5}{|c|}{{\ct COMB} (General combustion parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct COMB} (General combustion parameters)} \\
\hline \hline
\endhead
{\ct AUTO\_IGNITION\_TEMPERATURE}               & Real          & Section~\ref{info:ignition}                           & $^\circ$C     &  -273 $^\circ$C      \\ \hline
{\ct CHECK\_REALIZABILITY}                      & Logical       & Section~\ref{info:chem_integration}                   &               & {\ct .FALSE.}        \\ \hline
{\ct EXTINCTION\_MODEL}                         & Character     & Section~\ref{info:extinction}                         &               & {\ct 'EXTINCTION 2'} \\ \hline
{\ct FIXED\_MIX\_TIME}                          & Real          & Section~\ref{info:turbulent_combustion}               &  s            &                      \\ \hline
{\ct FUEL\_C\_TO\_CO\_FRACTION}                 & Real          & Section~\ref{info:two-step_simple_chemistry}          &               &  2/3                 \\ \hline
{\ct FUEL\_H\_TO\_H2\_FRACTION}                 & Real          & Section~\ref{info:two-step_simple_chemistry}          &               &  0                   \\ \hline
%{\ct HRRPUV\_MAX\_SMV}                          & Real          & Section~\ref{}                                        &  kW/m$^3$     & 1200                 \\ \hline
{\ct INITIAL\_UNMIXED\_FRACTION}                & Real          & Section~\ref{info:turbulent_combustion}               &               & 1.0                  \\ \hline
{\ct LAMINAR\_FLAME\_SPEED}                     & Real          & $s_L$, Section~\ref{info:ignition}                    & m/s           & 0.4                  \\ \hline
{\ct MAX\_CHEMISTRY\_SUBSTEPS}                  & Integer       & Section~\ref{info:chem_integration}                   &               & 20                   \\ \hline
{\ct N\_FIXED\_CHEMISTRY\_SUBSTEPS}             & Integer       & Section~\ref{info:chem_integration}                   &               & -1                   \\ \hline
{\ct N\_SIMPLE\_CHEMISTRY\_REACTIONS}           & Integer       & Section~\ref{info:two-step_simple_chemistry}          &               & 1                    \\ \hline
{\ct ODE\_SOLVER}                               & Character     & Section~\ref{info:chem_integration}                   &               &                      \\ \hline
{\ct RICHARDSON\_ERROR\_TOLERANCE}              & Real          & Section~\ref{info:chem_integration}                   &               & 1.0 E-6              \\ \hline
{\ct SUPPRESSION}                               & Logical       & Section~\ref{info:extinction}                         &               & {\ct .TRUE.}         \\ \hline
{\ct TAU\_CHEM}                                 & Real          & Section~\ref{info:turbulent_combustion}               &               & 1.E-10               \\ \hline
{\ct TAU\_FLAME}                                & Real          & Section~\ref{info:turbulent_combustion}               &               & 1.E10                \\ \hline
\end{longtable}

\vspace{\baselineskip}



\section{\texorpdfstring{{\tt CSVF}}{CSVF} (Comma Separated Velocity Files)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Comma separated velocity files ({\ct CSVF} namelist group)]{For more information see Section~\ref{info:CSVF}.}
\label{tbl:CSVF} \\
\hline
\multicolumn{5}{|c|}{{\ct CSVF} (Comma Delimited Output Files)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct CSVF} (Comma Delimited Output Files)} \\
\hline \hline
\endhead
%{\ct CSVFILE}         & Character      & Section~\ref{info:??}                &            &        \\ \hline
{\ct PER\_MESH}       & Logical        & Section~\ref{info:velo_restart}      &            & .FALSE. \\ \hline
{\ct UVWFILE}         & Character      & Section~\ref{info:velo_restart}      &            &     \\ \hline
\end{longtable}

\vspace{\baselineskip}



\section{\texorpdfstring{{\tt CTRL}}{CTRL} (Control Function Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Control function parameters ({\ct CTRL} namelist group)]{For more information see Section~\ref{info:CTRL}.}
\label{tbl:CTRL} \\
\hline
\multicolumn{5}{|c|}{{\ct CTRL} (Control Function Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct CTRL} (Control Function Parameters)} \\
\hline \hline
\endhead
{\ct CONSTANT}            & Real       & Section~\ref{info:CONTROL_MATH}         &    &                        \\ \hline
%{\ct CYCLES}             & Integer     & Number of times to cycle output             &    &                    \\ \hline
%{\ct CYCLE\_TIME}        & Real        & Periodicity                                 & s  &                    \\ \hline
{\ct DELAY}              & Real        & Section~\ref{info:dry_pipe}             & s  &  0.                    \\ \hline
{\ct DIFFERENTIAL\_GAIN} & Real        & Section~\ref{info:CONTROL_PID}          &    &  0.                    \\ \hline
{\ct EVACUATION}         & Logical     & Reference~\cite{FDS_Evac_Users_Guide}   &    & {\ct .FALSE.}          \\ \hline
{\ct FUNCTION\_TYPE}     & Character   & Section~\ref{info:basic_control}        &    &                        \\ \hline
{\ct ID}                 & Character   & Section~\ref{info:CTRL}                 &    &                        \\ \hline
{\ct INITIAL\_STATE}     & Logical     & Section~\ref{info:basic_control}        &    & {\ct .FALSE.}          \\ \hline
{\ct INPUT\_ID}          & Char.~Array & Section~\ref{info:CTRL}                 &    &                        \\ \hline
{\ct INTEGRAL\_GAIN}     & Real        & Section~\ref{info:CONTROL_PID}          &    &  0.                    \\ \hline
{\ct LATCH}              & Logical     & Section~\ref{info:basic_control}        &    & {\ct .TRUE.}           \\ \hline
{\ct N}                  & Integer     & Section~\ref{info:CTRL}                 &    &   1                    \\ \hline
{\ct ON\_BOUND}          & Character   & Section~\ref{info:DEADBAND}             &    & {\ct LOWER}            \\ \hline
{\ct PROPORTIONAL\_GAIN} & Real        & Section~\ref{info:CONTROL_PID}          &    &  0.                    \\ \hline
{\ct RAMP\_ID}           & Character   & Section~\ref{info:CUSTOM}               &    &                        \\ \hline
{\ct SETPOINT(2)}        & Real        & Section~\ref{info:basic_control}        &    &                        \\ \hline
{\ct TARGET\_VALUE}      & Real        & Section~\ref{info:CONTROL_PID}          &    &  0.                    \\ \hline
{\ct TRIP\_DIRECTION}    & Integer     & Section~\ref{info:basic_control}        &    &   1                    \\ \hline
\end{longtable}


\vspace{\baselineskip}


\section{\texorpdfstring{{\tt DEVC}}{DEVC} (Device Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Device parameters ({\ct DEVC} namelist group)]{For more information see Section~\ref{info:DEVC}.}
\label{tbl:DEVC} \\
\hline
\multicolumn{5}{|c|}{{\ct DEVC} (Device Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct DEVC} (Device Parameters)} \\
\hline \hline
\endhead
{\ct ABSOLUTE\_VALUE}       & Logical         & Section~\ref{info:out:DEVC}                                     &       & {\ct .FALSE.} \\ \hline
{\ct BYPASS\_FLOWRATE}      & Real            & Section~\ref{info:aspiration_detector}                          & kg/s  & 0             \\ \hline
{\ct CONVERSION\_ADDEND}    & Real            & Section~\ref{info:out:DEVC}                                     &       & 0             \\ \hline
{\ct CONVERSION\_FACTOR}    & Real            & Section~\ref{info:out:DEVC}                                     &       & 1             \\ \hline
{\ct COORD\_FACTOR}         & Real            & Section~\ref{info:line_file}                                    &       & 1             \\ \hline
{\ct CTRL\_ID}              & Character       & Section~\ref{info:RAMPDEVC}                                     &       &               \\ \hline
{\ct DELAY}                 & Real            & Section~\ref{info:aspiration_detector}                          & s     & 0             \\ \hline
{\ct DEPTH}                 & Real            & Section~\ref{info:material_components}                          & m     & 0             \\ \hline
{\ct DEVC\_ID}              & Character       & Sections~\ref{info:aspiration_detector} and \ref{info:RAMPDEVC} &       &               \\ \hline
{\ct D\_ID}                 & Character       & Section~\ref{info:line_file}                                    &       &               \\ \hline
{\ct DRY}                   & Logical         & Section~\ref{info:dry}                                          &       & {\ct .FALSE.} \\ \hline
{\ct DUCT\_ID}              & Character       & Section~\ref{info:HVAC}                                         &       &               \\ \hline
{\ct EVACUATION}            & Logical         & Reference~\cite{FDS_Evac_Users_Guide}                           &       & {\ct .FALSE.} \\ \hline
{\ct FLOWRATE}              & Real            & Section~\ref{info:aspiration_detector}                          & kg/s  & 0             \\ \hline
{\ct FORCE\_DIRECTION} & Real(3)     & Section~\ref{info:distributed_forces}                            &          &           \\ \hline
{\ct HIDE\_COORDINATES}     & Logical         & Section~\ref{info:line_file}                                    &       & {\ct .FALSE.} \\ \hline
{\ct ID}                    & Character       & Section~\ref{info:DEVC}                                         &       &               \\ \hline
{\ct INITIAL\_STATE}        & Logical         & Section~\ref{info:basic_control}                                &       & {\ct .FALSE.} \\ \hline
{\ct INIT\_ID}              & Character       & Section~\ref{info:PART_SURF}                                    &       &               \\ \hline
{\ct IOR}                   & Integer         & Section~\ref{info:DEVC}                                         &       &               \\ \hline
{\ct LATCH}                 & Logical         & Section~\ref{info:basic_control}                                &       & {\ct .TRUE.}  \\ \hline
{\ct MATL\_ID}              & Character       & Section~\ref{info:material_components}                          &       &               \\ \hline
{\ct N\_INTERVALS}          & Integer         & Section~\ref{info:time_integral}                                &       & 10            \\ \hline
{\ct NODE\_ID}              & Character(2)    & Section~\ref{info:HVAC}                                         &       &               \\ \hline
{\ct NO\_UPDATE\_DEVC\_ID}  & Character       & Section~\ref{info:freeze_device}                                &       &               \\ \hline
{\ct NO\_UPDATE\_CTRL\_ID}  & Character       & Section~\ref{info:freeze_device}                                &       &               \\ \hline
{\ct ORIENTATION}           & Real Triplet    & Section~\ref{info:DEVC}                                         &       & 0,0,-1        \\ \hline
{\ct ORIENTATION\_NUMBER}   & Integer         & Section~\ref{info:part_output}                                  &       & 1             \\ \hline
{\ct OUTPUT}                & Logical         & Section~\ref{info:out:DEVC}                                     &       & {\ct .TRUE.}  \\ \hline
{\ct PART\_ID}              & Character       & Section~\ref{info:outputquantities}                             &       &               \\ \hline
{\ct PIPE\_INDEX}           & Integer         & Section~\ref{info:pressureramp}                                 &       &  1            \\ \hline
{\ct POINTS}                & Integer         & Section~\ref{info:line_file}                                    &       & 1             \\ \hline
{\ct PROP\_ID}              & Character       & Section~\ref{info:DEVC}                                         &       &               \\ \hline
{\ct QUANTITY}              & Character       & Section~\ref{info:DEVC}                                         &       &               \\ \hline
{\ct QUANTITY2}             & Character       & Section~\ref{info:line_file}                                    &       &               \\ \hline
{\ct QUANTITY\_RANGE}       & Real(2)         & Section~\ref{info:statistics}                                   &       & -1.E50,1.E50  \\ \hline
{\ct RELATIVE}              & Logical         & Section~\ref{info:out:DEVC}                                     &       & {\ct .FALSE.} \\ \hline
{\ct R\_ID}                 & Character       & Section~\ref{info:line_file}                                    &       &               \\ \hline
{\ct ROTATION}              & Real            & Section~\ref{info:DEVC}                                         & deg.  & 0             \\ \hline
{\ct SETPOINT}              & Real            & Section~\ref{info:basic_control}                                &       &               \\ \hline
{\ct SPATIAL\_STATISTIC}    & Character       & Section~\ref{info:statistics}                                   &       &               \\ \hline
{\ct STATISTICS\_START}     & Real            & Section~\ref{info:rmscovcorr}                                   & s     & {\ct T\_BEGIN}\\ \hline
{\ct STATISTICS\_END}       & Real            & Section~\ref{info:rmscovcorr}                                   & s     & {\ct T\_BEGIN}\\ \hline
{\ct SMOOTHING\_FACTOR}     & Real            & Section~\ref{info:basic_control}                                &       & 0             \\ \hline
{\ct SPEC\_ID}              & Character       & Section~\ref{info:outputquantities}                             &       &               \\ \hline
{\ct SURF\_ID}              & Character       & Section~\ref{info:statistics}                                   &       &               \\ \hline
{\ct TEMPORAL\_STATISTIC}   & Character       & Section~\ref{info:statistics}                                   &       &               \\ \hline
{\ct TIME\_HISTORY}         & Logical         & Section~\ref{info:line_file}                                    &       &               \\ \hline
{\ct TIME\_PERIOD}          & Real            & Section~\ref{info:time_integral}                                & s     &               \\ \hline
{\ct TRIP\_DIRECTION}       & Integer         & Section~\ref{info:basic_control}                                &       &  1            \\ \hline
{\ct UNITS}                 & Character       & Section~\ref{info:out:DEVC}                                     &       &               \\ \hline
{\ct VELO\_INDEX}           & Integer         & Section~\ref{info:velocity}                                     &       &  0            \\ \hline
{\ct XB(6)}                 & Real Sextuplet  & Section~\ref{info:statistics}                                   & m     &               \\ \hline
{\ct XYZ(3)}                & Real Triplet    & Section~\ref{info:DEVC}                                         & m     &               \\ \hline
{\ct X\_ID}                 & Character       & Section~\ref{info:line_file}                                    &       &  {\ct ID-x}   \\ \hline
{\ct Y\_ID}                 & Character       & Section~\ref{info:line_file}                                    &       &  {\ct ID-y}   \\ \hline
{\ct Z\_ID}                 & Character       & Section~\ref{info:line_file}                                    &       &  {\ct ID-z}   \\ \hline
{\ct XYZ\_UNITS}            & Character       & Section~\ref{info:line_file}                                    &       &  {\ct 'm'}    \\ \hline
\end{longtable}


\vspace{\baselineskip}



\section{\texorpdfstring{{\tt DUMP}}{DUMP} (Output Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Output control parameters ({\ct DUMP} namelist group)]{For more information see Section~\ref{info:DUMP}.}
\label{tbl:DUMP} \\
\hline
\multicolumn{5}{|c|}{{\ct DUMP} (Output Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct DUMP} (Output Parameters)} \\
\hline \hline
\endhead
{\ct CFL\_FILE}                     & Logical      & Section~\ref{info:TIME_Control}        &           & {\ct .FALSE.}                  \\ \hline
{\ct CLIP\_RESTART\_FILES}          & Logical      & Section~\ref{info:restart}             &           & {\ct .TRUE.}                   \\ \hline
{\ct COLUMN\_DUMP\_LIMIT}           & Logical      & Section~\ref{info:out:DEVC}            &           & {\ct .FALSE.}                  \\ \hline
{\ct CTRL\_COLUMN\_LIMIT}           & Integer      & Section~\ref{info:out:DEVC}            &           & 254                            \\ \hline
%{\ct CUT\_CELL\_DATA\_FILE}        & Character    & Section~\ref{??}                       &           &                                \\ \hline
{\ct DEVC\_COLUMN\_LIMIT}           & Integer      & Section~\ref{info:out:DEVC}            &           & 254                            \\ \hline
%{\ct DT\_BNDE}                      & Real         & Section~\ref{info:DUMP}                &  s        & $2\,\Delta t${\ct /NFRAMES}    \\ \hline
{\ct DT\_BNDF}                      & Real         & Section~\ref{info:DUMP}                &  s        & $2\,\Delta t${\ct /NFRAMES}    \\ \hline
{\ct DT\_CPU}                       & Real         & Section~\ref{out:CPU}                  &  s        & 1000000                        \\ \hline
{\ct DT\_CTRL}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_DEVC}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_FLUSH}                     & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
%{\ct DT\_GEOM}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_HRR}                       & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_ISOF}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_MASS}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_PART}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_PL3D}                      & Real         & Section~\ref{info:DUMP}                &  s        & 1.E10                          \\ \hline
{\ct DT\_PROF}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct DT\_RESTART}                   & Real         & Section~\ref{info:DUMP}                &  s        & 1000000.                       \\ \hline
{\ct DT\_SL3D}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /5}             \\ \hline
{\ct DT\_SLCF}                      & Real         & Section~\ref{info:DUMP}                &  s        & $\Delta t${\ct /NFRAMES}       \\ \hline
{\ct EB\_PART\_FILE}                & Logical      & Section~\ref{out:PART}                 &           & {\ct .FALSE.}                  \\ \hline
{\ct FLUSH\_FILE\_BUFFERS}          & Logical      & Section~\ref{info:DUMP}                &           & {\ct .TRUE.}                   \\ \hline
{\ct MASS\_FILE}                    & Logical      & Section~\ref{info:DUMP}                &           & {\ct .FALSE.}                  \\ \hline
{\ct MAXIMUM\_PARTICLES}            & Integer      & Section~\ref{info:DUMP}                &           & 1000000                        \\ \hline
{\ct NFRAMES}                       & Integer      & Section~\ref{info:DUMP}                &           & 1000                           \\ \hline
{\ct PLOT3D\_PART\_ID(5)}           & Char.~Quint  & Section~\ref{info:PL3D}                &           &                                \\ \hline
{\ct PLOT3D\_QUANTITY(5)}           & Char.~Quint  & Section~\ref{info:PL3D}                &           &                                \\ \hline
{\ct PLOT3D\_SPEC\_ID(5)}           & Char.~Quint  & Section~\ref{info:PL3D}                &           &                                \\ \hline
{\ct PLOT3D\_VELO\_INDEX}           & Int.~Quint   & Section~\ref{info:velocity}            &           &  0                             \\ \hline
{\ct RENDER\_FILE}                  & Character    & Reference~\cite{Smokeview_Users_Guide} &           &                                \\ \hline
{\ct SIG\_FIGS}                     & Integer      & Section~\ref{info:SIG_FIGS}            &           & 8                              \\ \hline
{\ct SIG\_FIGS\_EXP}                & Integer      & Section~\ref{info:SIG_FIGS}            &           & 3                              \\ \hline
{\ct SMOKE3D}                       & Logical      & Section~\ref{info:SMOKE3D}             &           & {\ct .TRUE.}                   \\ \hline
{\ct SMOKE3D\_QUANTITY}             & Character    & Section~\ref{info:SMOKE3D}             &           &                                \\ \hline
{\ct SMOKE3D\_SPEC\_ID}             & Character    & Section~\ref{info:SMOKE3D}             &           &                                \\ \hline
{\ct STATUS\_FILES}                 & Logical      & Section~\ref{info:DUMP}                &           & {\ct .FALSE.}                  \\ \hline
%{\ct STORE\_SPECIES\_FLUX}          & Logical      & Section~\ref{info:DUMP}                &           & {\ct .FALSE.}                  \\ \hline
{\ct SUPPRESS\_DIAGNOSTICS}         & Logical      & Section~\ref{info:monitoring_progress} &           & {\ct .FALSE.}                  \\ \hline
{\ct UVW\_TIMER}                    & Real Vector (10)  & Section~\ref{info:velo_restart}   &  s        &                                \\ \hline
{\ct VELOCITY\_ERROR\_FILE}         & Logical      & Section~\ref{info:TIMING}              &           & {\ct .FALSE.}                  \\ \hline
{\ct WRITE\_XYZ}                    & Logical      & Section~\ref{info:PL3D}                &           & {\ct .FALSE.}                  \\ \hline
\end{longtable}

\noindent
$\Delta t$={\ct T\_END-T\_BEGIN}

\vspace{\baselineskip}

\section{\texorpdfstring{{\tt HEAD}}{HEAD} (Header Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Header parameters ({\ct HEAD} namelist group)]{For more information see Section~\ref{info:HEAD}.}
\label{tbl:HEAD} \\
\hline
\multicolumn{5}{|c|}{{\ct HEAD} (Header Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct HEAD} (Header Parameters)} \\
\hline \hline
\endhead
{\ct CHID}      & Character   & Section~\ref{info:HEAD}     &           & {\ct 'output'}    \\ \hline
{\ct TITLE}     & Character   & Section~\ref{info:PL3D}     &           &                   \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt HOLE}}{HOLE} (Obstruction Cutout Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Obstruction cutout parameters ({\ct HOLE} namelist group)]{For more information see Section~\ref{info:HOLE}.}
\label{tbl:HOLE} \\
\hline
\multicolumn{5}{|c|}{{\ct HOLE} (Obstruction Cutout Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct HOLE} (Obstruction Cutout Parameters)} \\
\hline \hline
\endhead
{\ct BLOCK\_WIND}  & Logical           & Section~\ref{info:BLOCK_WIND}                          &       &  {\ct .FALSE.}  \\ \hline
{\ct COLOR    }    & Character         & Section~\ref{info:colors}                              &       &                 \\ \hline
{\ct CTRL\_ID}     & Character         & Section~\ref{info:HOLE}                                &       &                 \\ \hline
{\ct DEVC\_ID}     & Character         & Section~\ref{info:HOLE}                                &       &                 \\ \hline
{\ct EVACUATION}   & Logical           & Reference~\cite{FDS_Evac_Users_Guide}                  &       &                 \\ \hline
{\ct ID }          & Character         & Identifier for input line                              &       &                 \\ \hline
{\ct MESH\_ID }    & Character         & Reference~\cite{FDS_Evac_Users_Guide}                  &       &                 \\ \hline
{\ct MULT\_ID }    & Character         & Section~\ref{info:MULT}                                &       &                 \\ \hline
{\ct RGB(3)   }    & Integer Triplet   & Section~\ref{info:colors}                              &       &                 \\ \hline
{\ct TRANSPARENCY} & Real              & Section~\ref{info:HOLE}                                &       &                 \\ \hline
{\ct XB(6)    }    & Real Sextuplet    & Section~\ref{info:MULT}                                & m     &                 \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt HVAC}}{HVAC} (HVAC System Definition)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[HVAC parameters ({\ct HVAC} namelist group)]{For more information see Section~\ref{info:HVAC}.}
\label{tbl:HVAC} \\
\hline
\multicolumn{5}{|c|}{{\ct HVAC} (HVAC System Definition)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct HVAC} (HVAC System Definition)} \\
\hline \hline
\endhead
{\ct AIRCOIL\_ID}               & Character         & Section~\ref{info:HVACduct}                                                   &               &                \\ \hline
{\ct AMBIENT}                   & Logical           & Section~\ref{info:HVACnode}                                                   &               & {\ct .FALSE.}  \\ \hline
{\ct AREA}                      & Real              & Section~\ref{info:HVACduct}                                                   & m$^2$         &                \\ \hline
{\ct CLEAN\_LOSS}               & Real              & Section~\ref{info:HVACfilter}                                                 &               &                \\ \hline
{\ct COOLANT\_MASS\_FLOW}       & Real              & Section~\ref{info:HVACaircoil}                                                & kg/s          &                \\ \hline
{\ct COOLANT\_SPECIFIC\_HEAT}   & Real              & Section~\ref{info:HVACaircoil}                                                & \si{kJ/(kg.K)} &               \\ \hline
{\ct COOLANT\_TEMPERATURE}      & Real              & Section~\ref{info:HVACaircoil}                                                & $^\circ$C     &                \\ \hline
{\ct CTRL\_ID}                  & Character         & Sections~\ref{info:HVACduct}, \ref{info:HVACfan}, \ref{info:HVACfilter}       &               &                \\ \hline
{\ct DAMPER}                    & Logical           & Sections~\ref{info:HVACduct}, \ref{info:HVACdamper}                           &               & {\ct .FALSE.}  \\ \hline
{\ct DEVC\_ID}                  & Character         & Sections ~\ref{info:HVACduct}, \ref{info:HVACfan}, \ref{info:HVACfilter}      &               &                \\ \hline
{\ct DIAMETER}                  & Real              & Section~\ref{info:HVACduct}                                                   &  m            &                \\ \hline
{\ct DUCT\_ID}                  & Char.~Array       & Section~\ref{info:HVACnode}                                                   &               &                \\ \hline
{\ct DUCT\_INTERP\_TYPE}        & Character         & Section~\ref{info:hvacmasstransport}                                          &               & {\ct 'NODE1'}  \\ \hline
{\ct EFFICIENCY}                & Real Array        & Sections~\ref{info:HVACfilter}, \ref{info:HVACaircoil}                        &               & 1.0            \\ \hline
{\ct FAN\_ID}                   & Character         & Section~\ref{info:HVACduct}                                                   &               &                \\ \hline
{\ct FILTER\_ID}                & Character         & Section~\ref{info:HVACnode}                                                   &               &                \\ \hline
{\ct FIXED\_Q}                  & Real              & Section~\ref{info:HVACaircoil}                                                & kW            &                \\ \hline
{\ct ID}                        & Character         & Section~\ref{info:HVAC}                                                       &               &                \\ \hline
{\ct LEAK\_ENTHALPY}            & Logical           & Section~\ref{info:local_leakage}                                              &               & {\ct .FALSE.}  \\ \hline
{\ct LENGTH}                    & Real              & Section~\ref{info:HVACduct}                                                   &  m            &                \\ \hline
{\ct LOADING}                   & Real Array        & Section ~\ref{info:HVACfilter}                                                & kg            & 0.0            \\ \hline
{\ct LOADING\_MULTIPLIER}       & Real Array        & Section ~\ref{info:HVACfilter}                                                & 1/kg          & 1.0            \\ \hline
{\ct LOSS}                      & Real Array        & Sections ~\ref{info:HVACduct} -- \ref{info:HVACfilter}                        &               & 0.0            \\ \hline
{\ct MASS\_FLOW  }              & Real              & Section~\ref{info:HVACduct}                                                   &  kg/s         &                \\ \hline
{\ct MAX\_FLOW}                 & Real              & Section ~\ref{info:HVACfan}                                                   &  m$^3$/s      &                \\ \hline
{\ct MAX\_PRESSURE}             & Real              & Section ~\ref{info:HVACfan}                                                   &  Pa           &                \\ \hline
{\ct N\_CELLS}                  & Integer           & Section~\ref{info:hvacmasstransport}                                          &               & 10*{\ct LENGTH} \\ \hline
{\ct NODE\_ID}                  & Char.~Doublet     & Section~\ref{info:HVACduct}                                                   &               &                \\ \hline
{\ct PERIMETER}                 & Real              & Section~\ref{info:HVACduct}                                                   &  m            &                \\ \hline
{\ct RAMP\_ID}                  & Character         & Sections ~\ref{info:HVACduct}, \ref{info:HVACfilter}, \ref{info:HVACfan}      &               &                \\ \hline
{\ct RAMP\_LOSS}                & Character         & Sections~\ref{info:HVACduct}, \ref{info:HVACdamper}                           &               &                \\ \hline
{\ct REVERSE}                   & Logical           & Section~\ref{info:HVACduct}                                                   &               & {\ct .FALSE.}  \\ \hline
{\ct ROUGHNESS}                 & Real              & Section~\ref{info:HVACduct}                                                   &  m            & 0.0            \\ \hline
{\ct SPEC\_ID}                  & Char.~Array       & Section ~\ref{info:HVACfilter}                                                &               &                \\ \hline
{\ct TAU\_AC}                   & Real              & Section ~\ref{info:HVACaircoil}                                               & s             & 1.0            \\ \hline
{\ct TAU\_FAN}                  & Real              & Section ~\ref{info:HVACfan}                                                   & s             & 1.0            \\ \hline
{\ct TAU\_VF}                   & Real              & Section~\ref{info:HVACduct}                                                   & s             & 1.0            \\ \hline
{\ct TYPE\_ID}                  & Character         & Section~\ref{info:HVAC}                                                       &               &                \\ \hline
{\ct VENT\_ID}                  & Character         & Section~\ref{info:HVACnode}                                                   &               &                \\ \hline
{\ct VENT2\_ID}                 & Character         & Section~\ref{info:local_leakage}                                              &               &                \\ \hline
{\ct VOLUME\_FLOW}              & Real              & Section~\ref{info:HVACduct}, \ref{info:HVACfan}                               &  m$^3$/s      &                \\ \hline
{\ct XYZ}                       & Real Triplet      & Section~\ref{info:HVACnode}                                                   &  m            &  0.0           \\ \hline
\end{longtable}


\vspace{\baselineskip}



\section{\texorpdfstring{{\tt INIT}}{INIT} (Initial Conditions)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Initial conditions ({\ct INIT} namelist group)]{For more information see Section~\ref{info:INIT}.}
\label{tbl:INIT} \\
\hline
\multicolumn{5}{|c|}{{\ct INIT} (Initial Conditions)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct INIT} (Initial Conditions)} \\
\hline \hline
\endhead
{\ct CELL\_CENTERED}              & Logical           & Section~\ref{info:initial_droplets}           &                & {\ct .FALSE.} \\ \hline
{\ct CTRL\_ID}                    & Character         & Section~\ref{info:initial_droplets}           &                &               \\ \hline
{\ct DENSITY}                     & Real              & Section~\ref{info:INIT}                       & kg/m$^3$       & Ambient       \\ \hline
{\ct DEVC\_ID}                    & Character         & Section~\ref{info:initial_droplets}           &                &               \\ \hline
{\ct DIAMETER}                    & Real              & Section~\ref{info:initial_droplets}           & \si{\micro m}  &               \\ \hline
{\ct DT\_INSERT}                  & Real              & Section~\ref{info:initial_droplets}           & s              &               \\ \hline
{\ct DX}                          & Real              & Section~\ref{info:initial_droplets}           & m              & 0.            \\ \hline
{\ct DY}                          & Real              & Section~\ref{info:initial_droplets}           & m              & 0.            \\ \hline
{\ct DZ}                          & Real              & Section~\ref{info:initial_droplets}           & m              & 0.            \\ \hline
{\ct HEIGHT}                      & Real              & Section~\ref{info:initial_droplets}           & m              &               \\ \hline
{\ct HRRPUV}                      & Real              & Section~\ref{info:INIT}                       & \si{kW/m^3}    &               \\ \hline
{\ct ID}                          & Character         & Section~\ref{info:PART_SURF}                  &                &               \\ \hline
{\ct MASS\_FRACTION(N)}           & Real Array        & Section~\ref{info:INIT}                       & kg/kg          & Ambient       \\ \hline
{\ct MASS\_PER\_TIME}             & Real              & Section~\ref{info:initial_droplets}           & kg/s           &               \\ \hline
{\ct MASS\_PER\_VOLUME}           & Real              & Section~\ref{info:initial_droplets}           & \si{kg/m^3}    & 1             \\ \hline
{\ct MULT\_ID }                   & Character         & Section~\ref{info:MULT}                       &                &               \\ \hline
{\ct N\_PARTICLES}                & Integer           & Section~\ref{info:initial_droplets}           &                & 0             \\ \hline
{\ct N\_PARTICLES\_PER\_CELL}     & Integer           & Section~\ref{info:initial_droplets}           &                & 0             \\ \hline
{\ct PACKING\_RATIO}              & Real              & Section~\ref{pine_needles}                    &                &               \\ \hline
{\ct PART\_ID}                    & Character         & Section~\ref{info:initial_droplets}           &                &               \\ \hline
{\ct PARTICLE\_WEIGHT\_FACTOR}    & Real              & Section~\ref{info:initial_droplets}           &                & 1.            \\ \hline
{\ct RADIUS}                      & Real              & Section~\ref{info:initial_droplets}           & m              &               \\ \hline
{\ct RAMP\_Q}                     & Character         & Section~\ref{info:init_hrrpuv}                &                &               \\ \hline
{\ct SHAPE}                       & Character         & Section~\ref{info:initial_droplets}           &                & {\ct 'BLOCK'} \\ \hline
{\ct SPEC\_ID(N)}                 & Character Array   & Section~\ref{info:INIT}                       &                &               \\ \hline
{\ct TEMPERATURE}                 & Real              & Section~\ref{info:INIT}                       & \si{\degree C} & {\ct TMPA}    \\ \hline
{\ct T\_INSERT}                   & Real              & Section~\ref{info:delayed_insertion}          & s              & {\ct T\_BEGIN}\\ \hline
{\ct UNIFORM}                     & Logical           & Section~\ref{info:initial_droplets}           &                & {\ct .FALSE.} \\ \hline
{\ct UVW(3)}                      & Real Triplet      & Section~\ref{info:initial_droplets}           & m/s            & 0.            \\ \hline
{\ct VOLUME\_FRACTION(N)}         & Real Array        & Section~\ref{info:INIT}                       & mol/mol        & Ambient       \\ \hline
{\ct XB(6)}                       & Real Sextuplet    & Section~\ref{info:INIT}                       & m              &               \\ \hline
{\ct XYZ(3)}                      & Real Triplet      & Section~\ref{info:initial_droplets}           & m              &               \\ \hline
\end{longtable}


\vspace{\baselineskip}



\section{\texorpdfstring{{\tt ISOF}}{ISOF} (Isosurface Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Isosurface parameters ({\ct ISOF} namelist group)]{For more information see Section~\ref{info:ISOF}.}
\label{tbl:ISOF} \\
\hline
\multicolumn{5}{|c|}{{\ct ISOF} (Isosurface Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct ISOF} (Isosurface Parameters)} \\
\hline \hline
\endhead
{\ct DELTA}                 & Real          & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct QUANTITY}              & Character     & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct QUANTITY2}             & Character     & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct REDUCE\_TRIANGLES}     & Integer       & Reference~\cite{Smokeview_Users_Guide}    &       & 1       \\ \hline
{\ct SPEC\_ID}              & Character     & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct SPEC\_ID2}             & Character     & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct SKIP}                  & Character     & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct SPEC\_ID}              & Character     & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct VALUE(I)}              & Real Array    & Section~\ref{info:ISOF}                   &       &         \\ \hline
{\ct VELO\_INDEX}           & Integer       & Section~\ref{info:velocity}               &       &  0      \\ \hline
{\ct VELO\_INDEX2}          & Integer       & Section~\ref{info:velocity}               &       &  0      \\ \hline
\end{longtable}


\vspace{\baselineskip}


\section{\texorpdfstring{{\tt MATL}}{MATL} (Material Properties)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Material properties ({\ct MATL} namelist group)]{For more information see Section~\ref{info:MATL}.}
\label{tbl:MATL} \\
\hline
\multicolumn{5}{|c|}{{\ct MATL} (Material Properties)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct MATL} (Material Properties)} \\
\hline \hline
\endhead
{\ct A(:)}                          & Real array      & Section~\ref{info:solid_pyrolysis}    &    1/s            &        \\ \hline
{\ct ABSORPTION\_COEFFICIENT}       & Real            & Section~\ref{info:thermal_properties} &    1/m            & 50000. \\ \hline
{\ct ALLOW\_SHRINKING}              & Logical         & Section~\ref{info:shrink_swell}       &                   & {\ct.TRUE.} \\ \hline
{\ct ALLOW\_SWELLING}               & Logical         & Section~\ref{info:shrink_swell}       &                   & {\ct.TRUE.} \\ \hline
{\ct ALPHA\_CHAR(:)}                & Real array      & Section~\ref{vegetation_model}        & kg/kg             & 1.     \\ \hline
{\ct BETA\_CHAR(:)}                 & Real array      & Section~\ref{vegetation_model}        & kg/kg             & 0.2     \\ \hline
{\ct BOILING\_TEMPERATURE}          & Real            & Section~\ref{info:liquid_fuels}       & $^\circ$C         & 5000.  \\ \hline
{\ct CONDUCTIVITY}                  & Real            & Section~\ref{info:thermal_properties} & \si{W/(m.K)}      & 0.     \\ \hline
{\ct CONDUCTIVITY\_RAMP}            & Character       & Section~\ref{info:thermal_properties} &                   &        \\ \hline
{\ct DENSITY}                       & Real            & Section~\ref{info:thermal_properties} & kg/m$^3$          & 0.     \\ \hline
{\ct DIFFUSIVITY\_SPEC(:)}          & Real            & Section~\ref{info:pyro3d}             & \si{m^2/2}        &        \\ \hline
{\ct E(:)}                          & Real array      & Section~\ref{info:solid_pyrolysis}    & J/mol             &        \\ \hline
{\ct EMISSIVITY    }                & Real            & Section~\ref{info:thermal_properties} &                   & 0.9    \\ \hline
{\ct GAS\_DIFFUSION\_DEPTH(:) }     & Real array      & Section~\ref{info:solid_pyrolysis}    & m                 & 0.001  \\ \hline
{\ct HEATING\_RATE(:)}              & Real array      & Section~\ref{info:solid_pyrolysis}    & $^\circ$C/min     & 5.     \\ \hline
{\ct HEAT\_OF\_COMBUSTION(:,:)}     & Real array      & Section~\ref{info:solid_pyrolysis}    & kJ/kg             &        \\ \hline
{\ct HEAT\_OF\_REACTION(:)}         & Real array      & Section~\ref{info:solid_pyrolysis}    & kJ/kg             & 0.     \\ \hline
{\ct HEAT\_OF\_REACTION\_RAMP(:)}  & Character array & Section~\ref{info:solid_pyrolysis}    &                   &        \\ \hline
{\ct ID     }                       & Character       & Section~\ref{info:SURF_MATL_Basics}   &                   &        \\ \hline
{\ct MATL\_ID(:,:)}                 & Character       & Section~\ref{info:solid_pyrolysis}    &                   &        \\ \hline
{\ct NU\_O2\_CHAR(:)}               & Real array      & Section~\ref{vegetation_model}        & kg/kg             & 0.     \\ \hline
{\ct NU\_MATL(:,:)}                 & Real array      & Section~\ref{info:solid_pyrolysis}    & kg/kg             & 0.     \\ \hline
{\ct NU\_SPEC(:,:)}                 & Real array      & Section~\ref{info:solid_pyrolysis}    & kg/kg             & 0.     \\ \hline
{\ct N\_REACTIONS}                  & Integer         & Section~\ref{info:solid_pyrolysis}    &                   & 0      \\ \hline
{\ct N\_O2(:)}                      & Real array      & Section~\ref{info:solid_pyrolysis}    &                   & 0.     \\ \hline
{\ct N\_S(:)}                       & Real array      & Section~\ref{info:solid_pyrolysis}    &                   & 1.     \\ \hline
{\ct N\_T(:)}                       & Real array      & Section~\ref{info:solid_pyrolysis}    &                   & 0.     \\ \hline
{\ct PCR(:)}                        & Logical array   & Section~\ref{info:solid_pyrolysis}    &                   & {\ct.FALSE.}\\ \hline
{\ct PYROLYSIS\_RANGE(:)}           & Real array      & Section~\ref{info:solid_pyrolysis}    & $^\circ$C         & 80.    \\ \hline
{\ct REFERENCE\_RATE(:)}            & Real array      & Section~\ref{info:solid_pyrolysis}    & 1/s               &        \\ \hline
{\ct REFERENCE\_TEMPERATURE(:)}     & Real array      & Section~\ref{info:solid_pyrolysis}    & $^\circ$C         &        \\ \hline
{\ct SPECIFIC\_HEAT}                & Real            & Section~\ref{info:thermal_properties} & \si{kJ/(kg.K)}    & 0.     \\ \hline
{\ct SPECIFIC\_HEAT\_RAMP}          & Character       & Section~\ref{info:thermal_properties} &                   &        \\ \hline
{\ct SPEC\_ID(:,:)}                 & Character       & Section~\ref{info:solid_pyrolysis}    &                   &        \\ \hline
{\ct THRESHOLD\_SIGN(:)}            & Real array      & Section~\ref{info:solid_pyrolysis}    &                   & 1.0    \\ \hline
{\ct THRESHOLD\_TEMPERATURE(:)}     & Real array      & Section~\ref{info:solid_pyrolysis}    & $^\circ$C         & -273.15 \\ \hline
\end{longtable}

\vspace{\baselineskip}



\section{\texorpdfstring{{\tt MESH}}{MESH} (Mesh Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Mesh parameters ({\ct MESH} namelist group)]{For more information see Section~\ref{info:MESH}.}
\label{tbl:MESH} \\
\hline
\multicolumn{5}{|c|}{{\ct MESH} (Mesh Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct MESH} (Mesh Parameters)} \\
\hline \hline
\endhead
{\ct CHECK\_MESH\_ALIGNMENT}         & Logical                       & Section~\ref{info:mesh_alignment}         &    & {\ct .FALSE.}    \\ \hline
{\ct COLOR}                          & Character                     & Section~\ref{info:multimesh}              &    & {\ct 'BLACK'}    \\ \hline
{\ct CYLINDRICAL}                    & Logical                       & Section~\ref{info:2D}                     &    & {\ct .FALSE.}    \\ \hline
{\ct EVACUATION}                     & Logical                       & Reference~\cite{FDS_Evac_Users_Guide}     &    & {\ct .FALSE.}    \\ \hline
{\ct EVAC\_HUMANS}                   & Logical                       & Reference~\cite{FDS_Evac_Users_Guide}     &    & {\ct .FALSE.}    \\ \hline
{\ct EVAC\_Z\_OFFSET}                & Real                          & Reference~\cite{FDS_Evac_Users_Guide}     & m  & 1                \\ \hline
{\ct ID}                             & Character                     & Reference~\cite{FDS_Evac_Users_Guide}     &    &                  \\ \hline
{\ct IJK}                            & Integer Triplet               & Section~\ref{info:MESH_Basics}            &    & 10,10,10         \\ \hline
{\ct LEVEL}                          & Integer                       & For future use                            &    & 0                \\ \hline
{\ct MPI\_PROCESS}                   & Integer                       & Section~\ref{info:multimesh}              &    &                  \\ \hline
{\ct N\_THREADS}                     & Integer                       & Section~\ref{info:multimesh}              &    &                  \\ \hline
{\ct MULT\_ID }                      & Character                     & Section~\ref{info:MULT}                   &    &                  \\ \hline
{\ct RGB}                            & Integer Triplet               & Section~\ref{info:multimesh}              &    & 0,0,0            \\ \hline
{\ct TRNX\_ID}                       & Character                     & Section~\ref{info:TRNX}                   &    &                  \\ \hline
{\ct TRNY\_ID}                       & Character                     & Section~\ref{info:TRNX}                   &    &                  \\ \hline
{\ct TRNZ\_ID}                       & Character                     & Section~\ref{info:TRNX}                   &    &                  \\ \hline
{\ct XB(6)}                          & Real Sextuplet                & Section~\ref{info:MESH_Basics}            & m  & 0,1,0,1,0,1      \\ \hline
\end{longtable}


\vspace{\baselineskip}



\section{\texorpdfstring{{\tt MISC}}{MISC} (Miscellaneous Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Miscellaneous parameters ({\ct MISC} namelist group)]{For more information see Section~\ref{info:MISC}.}
\label{tbl:MISC} \\
\hline
\multicolumn{5}{|c|}{{\ct MISC} (Miscellaneous Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct MISC} (Miscellaneous Parameters)} \\
\hline \hline
\endhead
%{\ct AEROSOL\_AL2O3}                            & Logical       &                                                       &               & {\ct .FALSE.}     \\ \hline
{\ct AGGLOMERATION}                             & Logical       & Section~\ref{info:agglomeration}                      &               & {\ct .TRUE.}      \\ \hline
{\ct \footnotesize ALLOW\_SURFACE\_PARTICLES}   & Logical       & Section~\ref{info:surface_droplets}                   &               & {\ct .TRUE.}      \\ \hline
{\ct \footnotesize ALLOW\_UNDERSIDE\_PARTICLES} & Logical       & Section~\ref{info:surface_droplets}                   &               & {\ct .FALSE.}     \\ \hline
{\ct \footnotesize ASSUMED\_GAS\_TEMPERATURE}   & Real          & Section~\ref{solid_phase_verification}                & $^\circ$C     &                   \\ \hline
{\ct \footnotesize ASSUMED\_GAS\_TEMPERATURE\_RAMP}& Character  & Section~\ref{solid_phase_verification}                &               &                   \\ \hline
{\ct BAROCLINIC}                                & Logical       & Section~\ref{baroclinic_torque}                       &               & {\ct .TRUE.}      \\ \hline
{\ct BNDF\_DEFAULT}                             & Logical       & Section~\ref{info:BNDF}                               &               & {\ct .TRUE.}      \\ \hline
%{\ct CC\_IBM}                                   & Logical       &                                                       &               & {\ct .FALSE.}     \\ \hline
{\ct C\_DEARDORFF}                              & Real          & Section~\ref{info:LES}                                &               & 0.1               \\ \hline
{\ct C\_SMAGORINSKY}                            & Real          & Section~\ref{info:LES}                                &               & 0.20              \\ \hline
{\ct C\_VREMAN}                                 & Real          & Section~\ref{info:LES}                                &               & 0.07              \\ \hline
{\ct C\_WALE}                                   & Real          & Section~\ref{info:LES}                                &               & 0.60              \\ \hline
{\ct CFL\_MAX}                                  & Real          & Section~\ref{info:CFL}                                &               & 1.0               \\ \hline
{\ct CFL\_MIN}                                  & Real          & Section~\ref{info:CFL}                                &               & 0.8               \\ \hline
{\ct CFL\_VELOCITY\_NORM}                       & Integer       & Section~\ref{info:CFL}                                &               &                   \\ \hline
{\ct CHECK\_HT}                                 & Logical       & Section~\ref{info:HT}                                 &               & {\ct .FALSE.}     \\ \hline
{\ct CHECK\_VN}                                 & Logical       & Section~\ref{info:VN}                                 &               & {\ct .TRUE.}      \\ \hline
{\ct CNF\_CUTOFF}                               & Real          & Section~\ref{info:particle_size}                      &               & 0.005             \\ \hline
{\ct \footnotesize CONSTANT\_SPECIFIC\_HEAT\_RATIO}  & Logical  & Section~\ref{info:Enthalpy}                           &               & {\ct .FALSE.}     \\ \hline
{\ct DEPOSITION}                                & Logical       & Section~\ref{info:deposition}                         &               & {\ct .TRUE.}      \\ \hline
{\ct EVACUATION\_DRILL}                         & Logical       & Reference~\cite{FDS_Evac_Users_Guide}                 &               & {\ct .FALSE.}     \\ \hline
{\ct EVACUATION\_MC\_MODE}                      & Logical       & Reference~\cite{FDS_Evac_Users_Guide}                 &               & {\ct .FALSE.}     \\ \hline
{\ct EVAC\_PRESSURE\_ITERATIONS}                & Integer       & Reference~\cite{FDS_Evac_Users_Guide}                 &               & 50                \\ \hline
{\ct EVAC\_TIME\_ITERATIONS}                    & Integer       & Reference~\cite{FDS_Evac_Users_Guide}                 &               & 50                \\ \hline
%{\ct POSITIVE\_ERROR\_TEST}                     & Logical       & Replace 'ERROR' with 'SUCCESS' label in stderr        &               &  {\ct .FALSE.}    \\ \hline
{\ct FLUX\_LIMITER}                             & Integer       & Section~\ref{info:flux_limiters}                      &               & 2                 \\ \hline
{\ct FREEZE\_VELOCITY}                          & Logical       & Section~\ref{info:freeze_velocity}                    &               & {\ct .FALSE.}     \\ \hline
{\ct GAMMA}                                     & Real          & Section~\ref{gas_species_props}                       &               & 1.4               \\ \hline
{\ct GRAVITATIONAL\_DEPOSITION}                 & Logical       & Section~\ref{info:deposition}                         &               & {\ct .TRUE.}      \\ \hline
{\ct GRAVITATIONAL\_SETTLING}                   & Logical       & Section~\ref{info:deposition}                         &               & {\ct .TRUE.}      \\ \hline
{\ct GVEC}                                      & Real triplet  & Section~\ref{info:GVEC}                               & m/s$^2$       & 0,0,-9.81         \\ \hline
{\ct H\_F\_REFERENCE\_TEMPERATURE}              & Real          & Section~\ref{info:enthalpy}                           & $^\circ$C     & 25.             \\ \hline
{\ct HVAC\_LOCAL\_PRESSURE}                    & Logical       & Section~\ref{info:HVAC}                               &              &  {\ct .TRUE.}     \\ \hline
{\ct HVAC\_MASS\_TRANSPORT}                     & Logical       & Section ~\ref{info:hvacmasstransport}                 &               & {\ct .FALSE.}     \\ \hline
{\ct HVAC\_PRES\_RELAX}                         & Real          & Section ~\ref{info:HVAC}                              &               & 0.5               \\ \hline
{\ct HUMIDITY}                                  & Real          & Section~\ref{info:humidity}                           & \%            & 40.               \\ \hline
{\ct IBLANK\_SMV}                               & Logical       & Section~\ref{info:SLCF}                               &               & {\ct .TRUE.}      \\ \hline
{\ct MAX\_LEAK\_PATHS}                          & Integer       & Section~\ref{info:Leaks}                              &               &  200              \\ \hline
{\ct MAXIMUM\_VISIBILITY}                       & Real          & Section~\ref{info:visibility}                         &  m            &  30               \\ \hline
{\ct MPI\_TIMEOUT}                              & Real          & Section~\ref{info:TIMING}                             &  s            & 10.               \\ \hline
{\ct NEAR\_WALL\_TURBULENCE\_MODEL}             & Character     & Section~\ref{info:LES}                                &               &                   \\ \hline
{\ct NOISE}                                     & Logical       & Section~\ref{info:NOISE}                              &               & {\ct .TRUE.}      \\ \hline
{\ct NOISE\_VELOCITY}                           & Real          & Section~\ref{info:NOISE}                              &  m/s          & 0.005             \\ \hline
{\ct NO\_EVACUATION}                            & Logical       & Reference~\cite{FDS_Evac_Users_Guide}                 &               & {\ct .FALSE.}     \\ \hline
{\ct NO\_RAMPS}                                 & Logical       & Turn off all ramps                                    &               & {\ct .FALSE.}     \\ \hline
{\ct OVERWRITE}                                 & Logical       & Section~\ref{info:OVERWRITE}                          &               & {\ct .TRUE.}      \\ \hline
{\ct PARTICLE\_CFL}                             & Logical       & Section~\ref{info:PART_Stability}                     &               & {\ct .FALSE.}     \\ \hline
{\ct PARTICLE\_CFL\_MAX}                        & Real          & Section~\ref{info:PART_Stability}                     &               & 1.0               \\ \hline
%{\ct PERIODIC\_TEST}                            & Integer       & Initial condition for verification test               &               & 0                 \\ \hline
{\ct POROUS\_FLOOR}                             & Logical       & Section~\ref{info:sprinklers}                         &               & {\ct .TRUE.}      \\ \hline
{\ct PR}                                        & Real          & Section~\ref{info:LES}                                &               & 0.5               \\ \hline
{\ct PROCESS\_ALL\_MESHES}                      & Logical       & Section~\ref{sec:periodic}                            &               & {\ct .FALSE.}     \\ \hline
%{\ct PROCESS\_CUTCELLS}                         & Logical       &                                                       &               & {\ct .TRUE.}     \\ \hline
{\ct PROJECTION}                                & Logical       & Section~\ref{info:CSVF}                               &               & {\ct .FALSE.}     \\ \hline
{\ct P\_INF}                                    & Real          & Section~\ref{info:MISC_Basics}                        & Pa            & 101325            \\ \hline
{\ct RAMP\_GX}                                  & Character     & Section~\ref{info:GVEC}                               &               &                   \\ \hline
{\ct RAMP\_GY}                                  & Character     & Section~\ref{info:GVEC}                               &               &                   \\ \hline
{\ct RAMP\_GZ}                                  & Character     & Section~\ref{info:GVEC}                               &               &                   \\ \hline
{\ct RESTART}                                   & Logical       & Section~\ref{info:restart}                            &               & {\ct .FALSE.}     \\ \hline
{\ct RESTART\_CHID}                             & Character     & Section~\ref{info:restart}                            &               & {\ct CHID}        \\ \hline
{\ct SC}                                        & Real          & Section~\ref{info:LES}                                &               & 0.5               \\ \hline
{\ct SIMULATION\_MODE}                          & Character     & Section~\ref{Sim_Mode}                                &               & {\ct 'VLES'}      \\ \hline
{\ct SHARED\_FILE\_SYSTEM}                      & Logical       & Section~\ref{info:multimesh}                          &               & {\ct .TRUE.}      \\ \hline
{\ct SMOKE\_ALBEDO}                             & Real          & Reference~\cite{Smokeview_Users_Guide}                &               & 0.3               \\ \hline
{\ct SOOT\_OXIDATION}                           & Logical       & Section~\ref{info:deposition}                         &               & {\ct .FALSE.}      \\ \hline
{\ct SOLID\_PHASE\_ONLY}                        & Logical       & Section~\ref{solid_phase_verification}                &               & {\ct .FALSE.}     \\ \hline
%{\ct TENSOR\_DIFFUSIVITY}                       & Logical       &                                                       &               & {\ct .FALSE.}     \\ \hline
%{\ct TERRAIN\_CASE}                             & Logical       & See Wildland Fire User's Guide                        &               & {\ct .FALSE.}     \\ \hline
%{\ct TERRAIN\_IMAGE}                            & Character     & See Wildland Fire User's Guide                        &               &                   \\ \hline
{\ct TAU\_DEFAULT}                              & Real          & Section~\ref{info:RAMP_Time}                          & s             & 1.                \\ \hline
{\ct TEXTURE\_ORIGIN(3)}                        & Real Triplet  & Section~\ref{info:texture_map}                        & m             & (0.,0.,0.)        \\ \hline
{\ct THERMOPHORETIC\_DEPOSITION}                & Logical       & Section~\ref{info:deposition}                         &               & {\ct .TRUE.}      \\ \hline
{\ct THERMOPHORETIC\_SETTLING}                  & Logical       & Section~\ref{info:deposition}                         &               & {\ct .TRUE.}      \\ \hline
{\ct THICKEN\_OBSTRUCTIONS}                     & Logical       & Section~\ref{info:OBST_Basics}                        &               & {\ct .FALSE.}     \\ \hline
{\ct TMPA}                                      & Real          & Section~\ref{info:MISC_Basics}                        & $^\circ$C     & 20.               \\ \hline
{\ct TURBULENCE\_MODEL}                         & Character     & Section~\ref{info:LES}                                &               & {\ct 'DEARDORFF'} \\ \hline
{\ct TURBULENT\_DEPOSITION}                     & Logical       & Section~\ref{info:deposition}                         &               & {\ct .TRUE.}      \\ \hline
%{\ct UVW\_FILE}                                 & Character     & See FDS Verification Guide                            &               &                   \\ \hline
%{\ct VEG\_LEVEL\_SET                            & Logical       & See Wildland Fire User's Guide                        &               & {\ct .FALSE.}     \\ \hline
{\ct VERBOSE}                                   & Logical       & Section~\ref{info:multimesh}                          &               &                   \\ \hline
{\ct VISIBILITY\_FACTOR}                        & Real          & Section~\ref{info:visibility}                         &               & 3                 \\ \hline
{\ct VN\_MAX}                                   & Real          & Section~\ref{info:VN}                                 &               & 1.0               \\ \hline
{\ct VN\_MIN}                                   & Real          & Section~\ref{info:VN}                                 &               & 0.8               \\ \hline
{\ct Y\_CO2\_INFTY}                             & Real          & Section~\ref{info:simple_chemistry}                   &  kg/kg        &                   \\ \hline
{\ct Y\_O2\_INFTY}                              & Real          & Section~\ref{info:simple_chemistry}                   &  kg/kg        &                   \\ \hline
%{\ct WIND\_ONLY}                                & Logical       & See Wildland Fire User's Guide                        &               & {\ct .FALSE.}     \\ \hline
\end{longtable}


\vspace{\baselineskip}


\section{\texorpdfstring{{\tt MOVE}}{MOVE} (Coordinate Transformation Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Coordinate transformation parameters ({\ct MULT} namelist group)]{For more information see Section~\ref{info:MOVE}.}
\label{tbl:MOVE} \\
\hline
\multicolumn{5}{|c|}{{\ct MOVE} (Coordinate Transformation Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct MOVE} (Coordinate Transformation Parameters)} \\
\hline \hline
\endhead
{\ct AXIS(1:3)}       & Real Triplet     & Axis of rotation                                &        & (0,0,1)                    \\ \hline
{\ct DX}              & Real             & Translation in the $x$ direction                & m      & 0.                         \\ \hline
{\ct DY}              & Real             & Translation in the $y$ direction                & m      & 0.                         \\ \hline
{\ct DZ}              & Real             & Translation in the $z$ direction                & m      & 0.                         \\ \hline
{\ct ID }             & Character        & Identification tag                              &        &                            \\ \hline
{\ct ROTATION\_ANGLE} & Real             & Angle of rotation about {\ct AXIS}              & deg.   & 0.                         \\ \hline
{\ct X0}              & Real             & $x$ origin                                      & m      & 0.                         \\ \hline
{\ct Y0}              & Real             & $y$ origin                                      & m      & 0.                         \\ \hline
{\ct Z0}              & Real             & $z$ origin                                      & m      & 0.                         \\ \hline
\end{longtable}


\vspace{\baselineskip}

\section{\texorpdfstring{{\tt MULT}}{MULT} (Multiplier Function Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Multiplier function parameters ({\ct MULT} namelist group)]{For more information see Section~\ref{info:MULT}.}
\label{tbl:MULT} \\
\hline
\multicolumn{5}{|c|}{{\ct MULT} (Multiplier Function Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct MULT} (Multiplier Function Parameters)} \\
\hline \hline
\endhead
{\ct DX}             & Real             & Spacing in the $x$ direction                & m  & 0.                         \\ \hline
{\ct DXB}            & Real Sextuplet   & Spacing for all 6 coordinates               & m  & 0.                         \\ \hline
{\ct DX0}            & Real             & Translation in the $x$ direction            & m  & 0.                         \\ \hline
{\ct DY}             & Real             & Spacing in the $y$ direction                & m  & 0.                         \\ \hline
{\ct DY0}            & Real             & Translation in the $y$ direction            & m  & 0.                         \\ \hline
{\ct DZ}             & Real             & Spacing in the $z$ direction                & m  & 0.                         \\ \hline
{\ct DZ0}            & Real             & Translation in the $z$ direction            & m  & 0.                         \\ \hline
{\ct ID }            & Character        & Identification tag                          &    &                            \\ \hline
{\ct I\_LOWER}       & Integer          & Lower array bound, $x$ direction            &    & 0                          \\ \hline
{\ct I\_LOWER\_SKIP} & Integer          & Lower array bound begin skip, $x$ direction &    &                            \\ \hline
{\ct I\_UPPER}       & Integer          & Upper array bound, $x$ direction            &    & 0                          \\ \hline
{\ct I\_UPPER\_SKIP} & Integer          & Upper array bound end skip, $x$ direction   &    &                            \\ \hline
{\ct J\_LOWER}       & Integer          & Lower array bound, $y$ direction            &    & 0                          \\ \hline
{\ct J\_LOWER\_SKIP} & Integer          & Lower array bound begin skip, $y$ direction &    &                            \\ \hline
{\ct J\_UPPER}       & Integer          & Upper array bound, $y$ direction            &    & 0                          \\ \hline
{\ct J\_UPPER\_SKIP} & Integer          & Upper array bound end skip, $y$ direction   &    &                            \\ \hline
{\ct K\_LOWER}       & Integer          & Lower array bound, $z$ direction            &    & 0                          \\ \hline
{\ct K\_LOWER\_SKIP} & Integer          & Lower array bound begin skip, $z$ direction &    &                            \\ \hline
{\ct K\_UPPER}       & Integer          & Upper array bound, $z$ direction            &    & 0                          \\ \hline
{\ct K\_UPPER\_SKIP} & Integer          & Upper array bound end skip, $z$ direction   &    &                            \\ \hline
{\ct N\_LOWER}       & Integer          & Lower sequence bound                        &    & 0                          \\ \hline
{\ct N\_LOWER\_SKIP} & Integer          & Lower sequence bound begin skip             &    &                            \\ \hline
{\ct N\_UPPER}       & Integer          & Upper sequence bound                        &    & 0                          \\ \hline
{\ct N\_UPPER\_SKIP} & Integer          & Upper sequence bound end skip               &    &                            \\ \hline
\end{longtable}


\vspace{\baselineskip}



\section{\texorpdfstring{{\tt OBST}}{OBST} (Obstruction Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Obstruction parameters ({\ct OBST} namelist group)]{For more information see Section~\ref{info:OBST}.}
\label{tbl:OBST} \\
\hline
\multicolumn{5}{|c|}{{\ct OBST} (Obstruction Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct OBST} (Obstruction Parameters)} \\
\hline \hline
\endhead
{\ct ALLOW\_VENT}         & Logical             & Section~\ref{info:OBST_Basics}            &           & {\ct .TRUE.}  \\ \hline
{\ct BNDF\_FACE(-3:3)}    & Logical Array       & Section~\ref{info:BNDF}                   &           & {\ct .TRUE.}  \\ \hline
{\ct BNDF\_OBST}          & Logical             & Section~\ref{info:BNDF}                   &           & {\ct .TRUE.}  \\ \hline
{\ct BULK\_DENSITY}       & Real                & Section~\ref{info:BURN_AWAY}              & kg/m$^3$  &               \\ \hline
{\ct COLOR    }           & Character           & Section~\ref{info:OBST_Basics}            &           &               \\ \hline
{\ct CTRL\_ID }           & Character           & Section~\ref{info:activate_deactivate}    &           &               \\ \hline
{\ct DEVC\_ID }           & Character           & Section~\ref{info:activate_deactivate}    &           &               \\ \hline
{\ct EVACUATION}          & Logical             & Reference~\cite{FDS_Evac_Users_Guide}     &           & {\ct .FALSE.} \\ \hline
{\ct HEIGHT}              & Real                & Section~\ref{info:multobst}               & m         &               \\ \hline
{\ct HT3D}                & Logical             & Section~\ref{info:ht3d}                   &           & {\ct .FALSE.} \\ \hline
{\ct ID }                 & Character           & Section~\ref{info:OBST_Basics}            &           &               \\ \hline
{\ct MESH\_ID}            & Character           & Reference~\cite{FDS_Evac_Users_Guide}     &           &               \\ \hline
{\ct MULT\_ID }           & Character           & Section~\ref{info:MULT}                   &           &               \\ \hline
%{\ct NOTERRAIN}           & Logical             & See Wildland Fire User's Guide            &           & {\ct .FALSE.} \\ \hline
{\ct ORIENTATION}         & Real Triplet        & Section~\ref{info:multobst}               & m         & (0.,0.,1.)    \\ \hline
{\ct OUTLINE}             & Logical             & Section~\ref{info:OBST_Basics}            &           & {\ct .FALSE.} \\ \hline
{\ct OVERLAY}             & Logical             & Section~\ref{info:OBST_Basics}            &           & {\ct .TRUE.}  \\ \hline
{\ct PERMIT\_HOLE}        & Logical             & Section~\ref{info:HOLE}                   &           & {\ct .TRUE.}  \\ \hline
{\ct PROP\_ID}            & Character           & Reference~\cite{Smokeview_Users_Guide}    &           &               \\ \hline
{\ct PYRO3D\_IOR}         & Integer             & Section~\ref{info:pyro3d}                 &           & 0             \\ \hline
%{\ct PYRO3D\_MASS\_TRANSPORT}  & Logical        & Section~\ref{info:pyro3d}                 &           & .FALSE.       \\ \hline
{\ct RADIUS}              & Real                & Section~\ref{info:multobst}               & m         &               \\ \hline
{\ct REMOVABLE}           & Logical             & Section~\ref{info:HOLE}                   &           & {\ct .TRUE.}  \\ \hline
{\ct RGB(3)}              & Integer Triplet     & Section~\ref{info:OBST_Basics}            &           &               \\ \hline
{\ct SHAPE}               & Character           & Section~\ref{info:multobst}               &           &               \\ \hline
{\ct SURF\_ID}            & Character           & Section~\ref{info:OBST_Basics}            &           &               \\ \hline
{\ct SURF\_ID6(6)}        & Character Sextuplet & Section~\ref{info:OBST_Basics}            &           &               \\ \hline
{\ct SURF\_IDS(3)}        & Character Triplet   & Section~\ref{info:OBST_Basics}            &           &               \\ \hline
{\ct TEXTURE\_ORIGIN(3)}  & Real Triplet        & Section~\ref{info:texture_map}            & m         & (0.,0.,0.)    \\ \hline
{\ct THICKEN}             & Logical             & Section~\ref{info:OBST_Basics}            &           & {\ct .FALSE.} \\ \hline
{\ct TRANSPARENCY}        & Real                & Section~\ref{info:OBST_Basics}            &           &  1            \\ \hline
{\ct XB(6) }              & Real Sextuplet      & Section~\ref{info:OBST_Basics}            & m         &               \\ \hline
{\ct XYZ(3) }             & Real Triplet        & Section~\ref{info:multobst}               & m         & (0.,0.,0.)    \\ \hline
\end{longtable}


\vspace{\baselineskip}


\section{\texorpdfstring{{\tt PART}}{PART} (Lagrangian Particles/Droplets)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Lagrangian particles ({\ct PART} namelist group)]{For more information see Chapter~\ref{info:PART}.}
\label{tbl:PART} \\
\hline
\multicolumn{5}{|c|}{{\ct PART} (Lagrangian Particles/Droplets)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct PART} (Lagrangian Particles/Droplets)} \\
\hline \hline
\endhead
{\ct AGE}                                & Real            & Section~\ref{info:part_output}          & s         & $1\times 10^5$ \\ \hline
{\ct BREAKUP}                            & Logical         & Section~\ref{info:secondary_breakup}    &           & {\ct .FALSE.} \\ \hline
{\ct BREAKUP\_CNF\_RAMP\_ID}             & Character       & Section~\ref{info:secondary_breakup}    &           &               \\ \hline
{\ct BREAKUP\_DISTRIBUTION}              & Character       & Section~\ref{info:secondary_breakup}    &           & {\ct 'ROSIN...'} \\ \hline
{\ct BREAKUP\_GAMMA\_D}                  & Real            & Section~\ref{info:secondary_breakup}    &           & 2.4           \\ \hline
{\ct BREAKUP\_RATIO}                     & Real            & Section~\ref{info:secondary_breakup}    &           & $3/7$         \\ \hline
{\ct BREAKUP\_SIGMA\_D}                  & Real            & Section~\ref{info:secondary_breakup}    &           &               \\ \hline
{\ct CHECK\_DISTRIBUTION}                & Logical         & Section~\ref{info:particle_size}        &           & {\ct .FALSE.} \\ \hline
{\ct CNF\_RAMP\_ID}                      & Character       & Section~\ref{info:particle_size}        &           &               \\ \hline
{\ct COLOR}                              & Character       & Section~\ref{info:part_output}          &           & {\ct 'BLACK'} \\ \hline
{\ct COMPLEX\_REFRACTIVE\_INDEX}         & Real            & Section~\ref{radiative_part_props}      &           & 0.01          \\ \hline
{\ct CTRL\_ID}                           & Character       & Section~\ref{info:particle_flux}        &           &               \\ \hline
{\ct DENSE\_VOLUME\_FRACTION}            & Real            & Section~\ref{info:DENSE_VOLUME_FRACTION}&           & $1\times 10^{-5}$ \\ \hline
{\ct DEVC\_ID}                           & Character       & Section~\ref{info:particle_flux}        &           &               \\ \hline
{\ct DIAMETER}                           & Real            & Section~\ref{info:particle_size}        & $\mu$m    &               \\ \hline
{\ct DISTRIBUTION}                       & Character       & Section~\ref{info:particle_size}        &           & {\ct 'ROSIN...'} \\ \hline
{\ct DRAG\_COEFFICIENT(3)}               & Real Array      & Section~\ref{info:particle_drag}        &           &               \\ \hline
{\ct DRAG\_LAW}                          & Character       & Section~\ref{info:particle_drag}        &           & {\ct 'SPHERE'}\\ \hline
% {\ct EMBER\_DENSITY\_THRESHOLD}          & Real            & experimental                            & \si{kg/m^3} & 0.0         \\ \hline
% {\ct EMBER\_PARTICLE}                    & Logical         & experimental                            &           & {\ct .FALSE.} \\ \hline
% {\ct EMBER\_VELOCITY\_THRESHOLD}         & Real            & experimental                            & m/s       & Infinite      \\ \hline
{\ct FREE\_AREA\_FRACTION}               & Real            & Section~\ref{info:particle_screen}      &           &               \\ \hline
{\ct GAMMA\_D}                           & Real            & Section~\ref{info:particle_size}        &           & 2.4           \\ \hline
{\ct HEAT\_OF\_COMBUSTION}               & Real            & Section~\ref{info:fuel_droplets}        & kJ/kg     &               \\ \hline
{\ct HORIZONTAL\_VELOCITY}               & Real            & Section~\ref{info:surface_droplets}     & m/s       &  0.2          \\ \hline
{\ct ID}                                 & Character       & Section~\ref{info:PART_Basics}          &           &               \\ \hline
{\ct INITIAL\_TEMPERATURE}               & Real            & Section~\ref{thermal_part_props}        & $^\circ$C & {\ct TMPA}    \\ \hline
{\ct MASSLESS}                           & Logical         & Section~\ref{info:MASSLESS}             &           & {\ct .FALSE.} \\ \hline
{\ct MAXIMUM\_DIAMETER}                  & Real            & Section~\ref{info:particle_size}        & $\mu$m    & Infinite      \\ \hline
{\ct MINIMUM\_DIAMETER}                  & Real            & Section~\ref{info:particle_size}        & $\mu$m    & 20.           \\ \hline
{\ct MONODISPERSE}                       & Logical         & Section~\ref{info:particle_size}        &           & {\ct .FALSE.} \\ \hline
{\ct N\_STRATA}                          & Integer         & Section~\ref{info:particle_size}        &           & 6             \\ \hline
{\ct ORIENTATION(1:3,:)}                 & Real Array      & Section~\ref{info:PART_SURF}            &           &               \\ \hline
{\ct PERIODIC\_X}                        & Logical         & Section~\ref{info:periodic-particles}   &           & {\ct .FALSE.} \\ \hline
{\ct PERIODIC\_Y}                        & Logical         & Section~\ref{info:periodic-particles}   &           & {\ct .FALSE.} \\ \hline
{\ct PERIODIC\_Z}                        & Logical         & Section~\ref{info:periodic-particles}   &           & {\ct .FALSE.} \\ \hline
{\ct PERMEABILITY(3)}                    & Real Array      & Section~\ref{info:porous_media}         &           &               \\ \hline
{\ct POROUS\_VOLUME\_FRACTION}           & Real            & Section~\ref{info:porous_media}         &           &               \\ \hline
{\ct PROP\_ID}                           & Character       & Section~\ref{info:PART_Basics}          &           &               \\ \hline
{\ct QUANTITIES(10)}                     & Character       & Section~\ref{info:part_output}          &           &               \\ \hline
{\ct QUANTITIES\_SPEC\_ID(10)}           & Character       & Section~\ref{info:part_output}          &           &               \\ \hline
{\ct RADIATIVE\_PROPERTY\_TABLE}         & Real            & Section~\ref{radiative_part_props}      &           &               \\ \hline
{\ct REAL\_REFRACTIVE\_INDEX}            & Real            & Section~\ref{radiative_part_props}      &           & 1.33          \\ \hline
{\ct RGB(3)}                             & Integers        & Section~\ref{info:part_output}          &           &               \\ \hline
{\ct RUNNING\_AVERAGE\_FACTOR}           & Real            & Section~\ref{radiative_part_props}      &           & 0.5           \\ \hline
{\ct SAMPLING\_FACTOR}                   & Integer         & Section~\ref{info:part_output}          &           & 1             \\ \hline
{\ct SECOND\_ORDER\_PARTICLE\_TRANSPORT} & Logical         & Section~\ref{info:PART_Stability}       &           & {\ct .FALSE.} \\ \hline
{\ct SHAPE\_FACTOR}                      & Real            & Sections~\ref{info:particle_radiation_absorption}, \ref{pine_needles} &   &            \\ \hline
{\ct SIGMA\_D}                           & Real            & Section~\ref{info:particle_size}        &           &               \\ \hline
{\ct SPEC\_ID}                           & Character       & Section~\ref{thermal_part_props}        &           &               \\ \hline
{\ct STATIC}                             & Logical         & Section~\ref{info:PART_SURF}            &           & {\ct .FALSE.} \\ \hline
{\ct SURFACE\_TENSION}                   & Real            & Section~\ref{info:secondary_breakup}    & N/m       & $7.28 \times 10^{-2}$  \\ \hline
{\ct SURF\_ID}                           & Character       & Section~\ref{info:PART_SURF}            &           &               \\ \hline
{\ct TURBULENT\_DISPERSION}              & Logical         & Section~\ref{info:MASSLESS}             &           & {\ct .FALSE.} \\ \hline
{\ct VERTICAL\_VELOCITY}                 & Real            & Section~\ref{info:surface_droplets}     & m/s       &  0.5          \\ \hline
\end{longtable}

\vspace{\baselineskip}

\section{\texorpdfstring{{\tt PRES}}{PRES} (Pressure Solver Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Pressure solver parameters ({\ct PRES} namelist group)]{For more information see Section~\ref{info:PRES}.}
\label{tbl:PRES} \\
\hline
\multicolumn{5}{|c|}{{\ct PRES} (Pressure Solver Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct PRES} (Pressure Solver Parameters)} \\
\hline \hline
\endhead
{\ct CHECK\_POISSON}                & Logical       & Section~\ref{pressure_solver}           &               & {\ct .FALSE.}             \\ \hline
{\ct FISHPAK\_BC(3)}                & Integer       & Section~\ref{dancing_eddies}            &               &                           \\ \hline
{\ct ITERATION\_SUSPEND\_FACTOR}    & Real          & Section~\ref{pressure_solver}           & s             & 0.95                      \\ \hline
{\ct MAX\_PRESSURE\_ITERATIONS}     & Integer       & Section~\ref{pressure_solver}           &               & 10                        \\ \hline
{\ct PRESSURE\_RELAX\_TIME}         & Real          & Section~\ref{background_pressure}       & s             & 1.                        \\ \hline
{\ct PRESSURE\_TOLERANCE}           & Real          & Section~\ref{pressure_solver}           & s$^{-2}$      &                           \\ \hline
{\ct RELAXATION\_FACTOR}            & Real          & Section~\ref{background_pressure}       &               & 1.                        \\ \hline
{\ct SOLVER}                        & Character     & Section~\ref{optional_pressure_solver}  &               & {\ct 'FFT'}               \\ \hline
{\ct SUSPEND\_PRESSURE\_ITERATIONS} & Logical       & Section~\ref{pressure_solver}           &               & {\ct .TRUE.}              \\ \hline
{\ct VELOCITY\_TOLERANCE}           & Real          & Section~\ref{pressure_solver}           & m/s           &                           \\ \hline
\end{longtable}

% Undocumented: SCARC_METHOD , SCARC_KRYLOV , SCARC_MULTIGRID, SCARC_SMOOTH  , SCARC_PRECON,
%               SCARC_COARSE , SCARC_INITIAL, SCARC_STORAGE  , SCARC_ACCURACY, SCARC_DEBUG ,
%               SCARC_MULTIGRID_CYCLE, SCARC_MULTIGRID_LEVEL , SCARC_MULTIGRID_COARSENING  ,
%               SCARC_MULTIGRID_ITERATIONS  , SCARC_MULTIGRID_ACCURACY   ,
%               SCARC_KRYLOV_ITERATIONS     , SCARC_KRYLOV_ACCURACY      ,
%               SCARC_SMOOTH_ITERATIONS     , SCARC_SMOOTH_ACCURACY      , SCARC_SMOOTH_OMEGA,
%               SCARC_PRECON_ITERATIONS     , SCARC_PRECON_ACCURACY      , SCARC_PRECON_OMEGA,
%               SCARC_COARSE_ITERATIONS     , SCARC_COARSE_ACCURACY

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt PROF}}{PROF} (Wall Profile Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Wall profile parameters ({\ct PROF} namelist group)]{For more information see Section~\ref{info:PROF}.}
\label{tbl:PROF} \\
\hline
\multicolumn{5}{|c|}{{\ct PROF} (Wall Profile Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct PROF} (Wall Profile Parameters)} \\
\hline \hline
\endhead
{\ct FORMAT\_INDEX}         & Integer           & Section~\ref{info:PROF}      &            & 1     \\ \hline
{\ct ID}                    & Character         & Section~\ref{info:PROF}      &            &       \\ \hline
{\ct INIT\_ID}              & Character         & Section~\ref{info:PROF}      &            &       \\ \hline
{\ct IOR}                   & Real              & Section~\ref{info:PROF}      &            &       \\ \hline
{\ct QUANTITY}              & Character         & Section~\ref{info:PROF}      &            &       \\ \hline
{\ct XYZ}                   & Real Triplet      & Section~\ref{info:PROF}      & m          &       \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt PROP}}{PROP} (Device Properties)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Device properties ({\ct PROP} namelist group)]{For more information see Section~\ref{info:PROP}.}
\label{tbl:PROP} \\
\hline
\multicolumn{5}{|c|}{{\ct PROP} (Device Properties)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct PROP} (Device Properties)} \\
\hline \hline
\endhead
{\ct ACTIVATION\_OBSCURATION}           & Real          & Section~\ref{info:smoke_detector}         & \%/m                  & 3.24      \\ \hline
{\ct ACTIVATION\_TEMPERATURE}           & Real          & Section~\ref{info:sprinklers}             & $^\circ$C             & 74.        \\ \hline
{\ct ALPHA\_C}                          & Real          & Section~\ref{info:smoke_detector}         &                       & 1.8       \\ \hline
{\ct ALPHA\_E}                          & Real          & Section~\ref{info:smoke_detector}         &                       & 0.       \\ \hline
{\ct BETA\_C}                           & Real          & Section~\ref{info:smoke_detector}         &                       & 1.       \\ \hline
{\ct BETA\_E}                           & Real          & Section~\ref{info:smoke_detector}         &                       & 1.       \\ \hline
{\ct CHARACTERISTIC\_VELOCITY}          & Real          & Section~\ref{info:pressure_coefficient}   & m/s                   & 1.       \\ \hline
{\ct C\_FACTOR}                         & Real          & Section~\ref{info:sprinklers}             & (m/s)$^{1/2}$         & 0.        \\ \hline
{\ct DENSITY}                           & Real          & Section~\ref{info:THERMOCOUPLE}           & kg/m$^3$              & 8908.     \\ \hline
{\ct DIAMETER}                          & Real          & Section~\ref{info:THERMOCOUPLE}           & m                     & 0.001     \\ \hline
{\ct EMISSIVITY}                        & Real          & Section~\ref{info:THERMOCOUPLE}           &                       & 0.85      \\ \hline
{\ct FLOW\_RAMP}                        & Character     & Section~\ref{info:sprinklers}             &                       &           \\ \hline
{\ct FLOW\_RATE}                        & Real          & Section~\ref{info:sprinklers}             & L/min                 &           \\ \hline
{\ct FLOW\_TAU}                         & Real          & Section~\ref{info:sprinklers}             &                       & 0.       \\ \hline
{\ct GAUGE\_EMISSIVITY}                 & Real          & Section~\ref{info:heat_flux}              &                       & 1.        \\ \hline
{\ct GAUGE\_TEMPERATURE}                & Real          & Section~\ref{info:heat_flux}              & $^\circ$C             & {\ct TMPA}\\ \hline
{\ct HEAT\_TRANSFER\_COEFFICIENT}       & Real          & Section~\ref{info:THERMOCOUPLE}           & \si{W/(m$^2$.K)}      &           \\ \hline
{\ct ID}                                & Character     & Section~\ref{info:PROP}                   &                       &           \\ \hline
{\ct INITIAL\_TEMPERATURE}              & Real          & Section~\ref{info:sprinklers}             & $^\circ$C             & {\ct TMPA}\\ \hline
{\ct K\_FACTOR}                         & Real          & Section~\ref{info:sprinklers}             & $\si{L/(min.bar^{\ha})}$ & 1.        \\ \hline
{\ct LENGTH}                            & Real          & Section~\ref{info:smoke_detector}         & m                     & 1.8       \\ \hline
{\ct MASS\_FLOW\_RATE}                  & Real          & Section~\ref{info:sprinklers}             & kg/s                  &           \\ \hline
{\ct OFFSET}                            & Real          & Section~\ref{info:sprinklers}             & m                     & 0.05      \\ \hline
{\ct OPERATING\_PRESSURE}               & Real          & Section~\ref{info:sprinklers}             & bar                   & 1.        \\ \hline
{\ct ORIFICE\_DIAMETER}                 & Real          & Section~\ref{info:sprinklers}             & m                     & 0.       \\ \hline
{\ct P0,PX(3),PXX(3,3)}                 & Real          & Section~\ref{info:velocity_patch}         & m/s                   &  0.         \\ \hline
{\ct PARTICLES\_PER\_SECOND}            & Integer       & Section~\ref{info:sprinklers}             &                       & 5000      \\ \hline
{\ct PARTICLE\_VELOCITY}                & Real          & Section~\ref{info:sprinklers}             & m/s                   & 0.       \\ \hline
{\ct PART\_ID}                          & Character     & Section~\ref{info:sprinklers}             &                       &           \\ \hline
{\ct PDPA\_END}                         & Real          & Section~\ref{PDPA}                        & s                     & {\ct T\_END} \\ \hline
{\ct PDPA\_HISTOGRAM}                   & Logical       & Section~\ref{PDPA}                        &                       & .FALSE.   \\ \hline
{\ct PDPA\_HISTOGRAM\_CUMULATIVE}       & Logical       & Section~\ref{PDPA}                        &                       & .FALSE.   \\ \hline
{\ct PDPA\_HISTOGRAM\_LIMITS}           & Real Array    & Section~\ref{PDPA}                        &                       &       \\ \hline
{\ct PDPA\_HISTOGRAM\_NBINS}            & Integer       & Section~\ref{PDPA}                        &                       & 10        \\ \hline
{\ct PDPA\_INTEGRATE}                   & Logical       & Section~\ref{PDPA}                        &                       & {\ct .TRUE.}         \\ \hline
{\ct PDPA\_M}                           & Integer       & Section~\ref{PDPA}                        &                       & 0         \\ \hline
{\ct PDPA\_N}                           & Integer       & Section~\ref{PDPA}                        &                       & 0         \\ \hline
{\ct PDPA\_NORMALIZE}                   & Logical       & Section~\ref{PDPA}                        &                       & {\ct .TRUE.}         \\ \hline
{\ct PDPA\_RADIUS}                      & Real          & Section~\ref{PDPA}                        & m                     & 0.        \\ \hline
{\ct PDPA\_START}                       & Real          & Section~\ref{PDPA}                        & s                     & 0.        \\ \hline
{\ct PRESSURE\_RAMP}                    & Character     & Section~\ref{info:sprinklers}             &                       &           \\ \hline
{\ct QUANTITY}                          & Character     & Section~\ref{info:sprinklers}             &                       &           \\ \hline
{\ct RTI}                               & Real          & Section~\ref{info:sprinklers}             & $\sqrt{\si{m.s}}$     & 100.      \\ \hline
{\ct SMOKEVIEW\_ID}                     & Char.~Array   & Section~\ref{info:SMOKEVIEW_ID}           &                       &           \\ \hline
{\ct SMOKEVIEW\_PARAMETERS}             & Char.~Array   & Section~\ref{info:SMOKEVIEW_PARAMETERS}   &                       &           \\ \hline
{\ct SPEC\_ID}                          & Character     & Section~\ref{info:alternative_smoke}      &                       &           \\ \hline
{\ct SPECIFIC\_HEAT}                    & Real          & Section~\ref{info:THERMOCOUPLE}           & \si{kJ/(kg.K)}        & 0.44      \\ \hline
{\ct SPRAY\_ANGLE(2,2)}                 & Real          & Section~\ref{info:sprinklers}             & degrees               & 60.,75.   \\ \hline
{\ct SPRAY\_PATTERN\_BETA}              & Real          & Section~\ref{info:sprinklers}             & degrees               & 5.        \\ \hline
{\ct SPRAY\_PATTERN\_MU}                & Real          & Section~\ref{info:sprinklers}             & degrees               & 0.        \\ \hline
{\ct SPRAY\_PATTERN\_SHAPE}             & Character     & Section~\ref{info:sprinklers}             &                       & {\ct 'GAUSSIAN'}  \\ \hline
{\ct SPRAY\_PATTERN\_TABLE}             & Character     & Section~\ref{info:sprinklers}             &                       &           \\ \hline
{\ct VELOCITY\_COMPONENT}               & Integer       & Section~\ref{info:velocity_patch}         &                       &           \\ \hline
\end{longtable}


\vspace{\baselineskip}

\section{\texorpdfstring{{\tt RADF}}{RADF} (Radiation Output File Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Radiation output file parameters ({\ct RADF} namelist group)]{For more information see Section~\ref{info:RADF}.}
\label{tbl:RADF} \\
\hline
\multicolumn{5}{|c|}{{\ct RADF} (Radiation Output File Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct RADF} (Radiation Output File Parameters)} \\
\hline \hline
\endhead
{\ct I\_STEP}                       & Integer              & Section~\ref{info:RADF}            &                   &  1     \\ \hline
{\ct J\_STEP}                       & Integer              & Section~\ref{info:RADF}            &                   &  1     \\ \hline
{\ct K\_STEP}                       & Integer              & Section~\ref{info:RADF}            &                   &  1     \\ \hline
{\ct XB}                            & Real Sextuplet       & Section~\ref{info:RADF}            & m                 &        \\ \hline
\end{longtable}


\vspace{\baselineskip}

\section{\texorpdfstring{{\tt RADI}}{RADI} (Radiation Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Radiation parameters ({\ct RADI} namelist group)]{For more information see Section~\ref{info:RADI}.}
\label{tbl:RADI} \\
\hline
\multicolumn{5}{|c|}{{\ct RADI} (Radiation Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct RADI} (Radiation Parameters)} \\
\hline \hline
\endhead
{\ct ANGLE\_INCREMENT}              & Integer       & Section~\ref{info:RADI_Resolution}        &                   & 5                 \\ \hline
{\ct BAND\_LIMITS    }              & Real Array    & Section~\ref{info:RADI_Wide_Band}         & $\mu$m            &                   \\ \hline
{\ct C\_MAX                   }     & Real          & Section~\ref{info:CHI_R}                  &                   & 100               \\ \hline
{\ct C\_MIN                   }     & Real          & Section~\ref{info:CHI_R}                  &                   & 1                 \\ \hline
{\ct INITIAL\_RADIATION\_ITERATIONS}& Integer       & Section~\ref{info:RADI_Resolution}        &                   & 3                 \\ \hline
{\ct KAPPA0                   }     & Real          & Section~\ref{info:RADI_Absorption}        & 1/m               & 0                 \\ \hline
{\ct MIE\_MINIMUM\_DIAMETER}        & Real          & Section~\ref{info:RADI_Absorption}        & $\mu$m            & 0.5               \\ \hline
{\ct MIE\_MAXIMUM\_DIAMETER}        & Real          & Section~\ref{info:RADI_Absorption}        & $\mu$m            & 1.5$\times D$     \\ \hline
{\ct MIE\_NDG}                      & Integer       & Section~\ref{info:RADI_Absorption}        &                   & 50                \\ \hline
{\ct NMIEANG                  }     & Integer       & Section~\ref{info:RADI_Absorption}        &                   & 15                \\ \hline
{\ct NUMBER\_RADIATION\_ANGLES}     & Integer       & Section~\ref{info:RADI_Resolution}        &                   & 100               \\ \hline
{\ct OPTICALLY\_THIN}               & Logical       & Section~\ref{info:CHI_R}                  &                   & {\ct .FALSE.}     \\ \hline
{\ct PATH\_LENGTH }                 & Real          & Section~\ref{info:RADI_Wide_Band}         &   m               & 0.1               \\ \hline
{\ct QR\_CLIP                  }    & Real          & Section~\ref{info:CHI_R}                  & kW/m$^3$          & 10                \\ \hline
{\ct RADIATION}                     & Logical       & Section~\ref{info:radiation_off}          &                   & {\ct .TRUE.}      \\ \hline
{\ct RADIATION\_ITERATIONS}         & Integer       & Section~\ref{info:RADI_Resolution}        &                   & 1                 \\ \hline
{\ct RADTMP                   }     & Real          & Section~\ref{info:RADI_Absorption}        & $^\circ$C         & 900               \\ \hline
{\ct TIME\_STEP\_INCREMENT}         & Integer       & Section~\ref{info:RADI_Resolution}        &                   & 3                 \\ \hline
{\ct WIDE\_BAND\_MODEL    }         & Logical       & Section~\ref{info:RADI_Wide_Band}         &                   & {\ct .FALSE.}     \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt RAMP}}{RAMP} (Ramp Function Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Ramp function parameters ({\ct RAMP} namelist group)]{For more information see Chapter~\ref{info:RAMP}.}
\label{tbl:RAMP} \\
\hline
\multicolumn{5}{|c|}{{\ct RAMP} (Ramp Function Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct RAMP} (Ramp Function Parameters)} \\
\hline \hline
\endhead
{\ct CTRL\_ID}                      & Character     & Section~\ref{info:RAMPDEVC}   &                       &           \\ \hline
{\ct DEVC\_ID}                      & Character     & Section~\ref{info:RAMPDEVC}   &                       &           \\ \hline
{\ct F}                             & Real          & Chapter~\ref{info:RAMP}       &                       &           \\ \hline
{\ct ID}                            & Character     & Chapter~\ref{info:RAMP}       &                       &           \\ \hline
{\ct NUMBER\_INTERPOLATION\_POINTS} & Integer       & Chapter~\ref{info:RAMP}       &                       &  5000     \\ \hline
{\ct T}                             & Real          & Chapter~\ref{info:RAMP}       & s (or $^\circ$C)      &           \\ \hline
{\ct X}                             & Real          & Section~\ref{info:GVEC}       & m                     &           \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt REAC}}{REAC} (Reaction Parameters)}
\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Reaction parameters ({\ct REAC} namelist group)]{For more information see Chapter~\ref{chap:combustion}.}
\label{tbl:REAC} \\
\hline
\multicolumn{5}{|c|}{{\ct REAC} (Reaction Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct REAC} (Reaction Parameters)} \\
\hline \hline
\endhead
{\ct A}                                   & Real        & Section~\ref{info:finite}                 &                   &                   \\ \hline
{\ct AUTO\_IGNITION\_TEMPERATURE}         & Real        & Section~\ref{info:ignition}               & $^\circ$C         & -273 $^\circ$C    \\ \hline
{\ct C}                                   & Real        & Section~\ref{info:simple_chemistry}       &                   & 0                 \\ \hline
{\ct CHECK\_ATOM\_BALANCE}                & Logical     & Section~\ref{info:REAC_Diagnostics}       &                   & {\ct .TRUE.}      \\ \hline
{\ct CO\_YIELD}                           & Real        & Section~\ref{info:simple_chemistry}       & kg/kg             & 0                 \\ \hline
{\ct CRITICAL\_FLAME\_TEMPERATURE}        & Real        & Section~\ref{info:extinction}             &   $^\circ$C       & 1427              \\ \hline
{\ct E}                                   & Real        & Section~\ref{info:finite}                 &   J/mol           &                   \\ \hline
{\ct EPUMO2}                              & Real        & Section~\ref{info:heat_of_combustion}     &   kJ/kg           & 13100             \\ \hline
{\ct EQUATION}                            & Character   & Section~\ref{info:EQUATION}               &                   &                   \\ \hline
{\ct FORMULA}                             & Character   & Section~\ref{info:simple_chemistry}       &                   &                   \\ \hline
{\ct FUEL}                                & Character   & Section~\ref{info:simple_chemistry}       &                   &                   \\ \hline
{\ct FUEL\_RADCAL\_ID}                    & Character   & Section~\ref{info:simple_chemistry}       &                   &                   \\ \hline
{\ct H}                                   & Real        & Section~\ref{info:simple_chemistry}       &                   & 0                 \\ \hline
{\ct HEAT\_OF\_COMBUSTION}                & Real        & Section~\ref{info:heat_of_combustion}     & kJ/kg             &                   \\ \hline
{\ct HOC\_COMPLETE}                       & Real        & Section~\ref{info:hoc_complete}           & kJ/kg             &                   \\ \hline
{\ct ID}                                  & Character   & Section~\ref{info:simple_chemistry}       &                   &                   \\ \hline
{\ct IDEAL}                               & Logical     & Section~\ref{info:simple_chemistry}       &                   & {\ct .FALSE.}     \\ \hline
{\ct LOWER\_OXYGEN\_LIMIT}                & Real        & Section~\ref{info:extinction}             & mol/mol           &                   \\ \hline
{\ct N}                                   & Real        & Section~\ref{info:simple_chemistry}       &                   & 0                 \\ \hline
{\ct NU(:)}                               & Real Array  & Section~\ref{info:finite}                 &                   &                   \\ \hline
{\ct N\_S(:)}                             & Real Array  & Section~\ref{info:finite}                 &                   &                   \\ \hline
{\ct N\_T}                                & Real        & Section~\ref{info:finite}                 &                   &                   \\ \hline
{\ct O}                                   & Real        & Section~\ref{info:simple_chemistry}       &                   & 0                 \\ \hline
{\ct PRIORITY}                            & Integer     & Section~\ref{info:priority}               &                   & 1                 \\ \hline
{\ct RADIATIVE\_FRACTION}                 & Real        & Section~\ref{info:CHI_R}                  &                   &                   \\ \hline
{\ct RAMP\_CHI\_R}                        & Character   & Section~\ref{info:CHI_R}                  &                   &                   \\ \hline
{\ct REAC\_ATOM\_ERROR}                   & Real        & Section~\ref{info:REAC_Diagnostics}       & atoms             & 1.E-5             \\ \hline
{\ct REAC\_MASS\_ERROR}                   & Real        & Section~\ref{info:REAC_Diagnostics}       & kg/kg             & 1.E-4             \\ \hline
{\ct SOOT\_H\_FRACTION}                   & Real        & Section~\ref{info:simple_chemistry}       &                   & 0.1               \\ \hline
{\ct SOOT\_YIELD}                         & Real        & Section~\ref{info:simple_chemistry}       & kg/kg             & 0.0               \\ \hline
{\ct SPEC\_ID\_N\_S(:)}                   & Char.~Array & Section~\ref{info:finite}                 &                   &                   \\ \hline
{\ct SPEC\_ID\_NU(:)}                     & Char.~Array & Section~\ref{info:finite}                 &                   &                   \\ \hline
{\ct THIRD\_BODY}                         & Logical     & Section~\ref{info:finite}                 &                   & {\ct .FALSE.}     \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt SLCF}}{SLCF} (Slice File Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Slice file parameters ({\ct SLCF} namelist group)]{For more information see Section~\ref{info:SLCF}.}
\label{tbl:SLCF} \\
\hline
\multicolumn{5}{|c|}{{\ct SLCF} (Slice File Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct SLCF} (Slice File Parameters)} \\
\hline \hline
\endhead
{\ct CELL\_CENTERED}    & Logical           & Section~\ref{info:SLCF}                   &           & {\ct .FALSE.}     \\ \hline
{\ct EVACUATION}        & Logical           & Reference~\cite{FDS_Evac_Users_Guide}     &           & {\ct .FALSE.}\\ \hline
{\ct MAXIMUM\_VALUE}    & Real              & Reference~\cite{Smokeview_Users_Guide}    &           &                   \\ \hline
{\ct MESH\_NUMBER}      & Integer           & Section~\ref{info:SLCF}                   &           &                   \\ \hline
{\ct MINIMUM\_VALUE}    & Real              & Reference~\cite{Smokeview_Users_Guide}    &           &                   \\ \hline
{\ct PART\_ID}          & Character         & Section~\ref{info:outputquantities}       &           &                   \\ \hline
{\ct PBX, PBY, PBZ}     & Real              & Section~\ref{info:SLCF}                   & m         &                   \\ \hline
{\ct QUANTITY}          & Character         & Section~\ref{info:outputquantities}       &           &                   \\ \hline
{\ct QUANTITY2}         & Character         & Section~\ref{info:outputquantities}       &           &                   \\ \hline
{\ct SPEC\_ID}          & Character         & Section~\ref{info:outputquantities}       &           &                   \\ \hline
{\ct VECTOR    }        & Logical           & Section~\ref{info:SLCF}                   &           & {\ct .FALSE.}     \\ \hline
{\ct VELO\_INDEX}       & Integer           & Section~\ref{info:velocity}               &           &  0                \\ \hline
{\ct XB(6)}             & Real Sextuplet    & Section~\ref{info:SLCF}                   & m         &                   \\ \hline
\end{longtable}

%Undocumented: AGL_SLICE,FIRE_LINE, ID, LEVEL_SET_FIRE_LINE

\vspace{\baselineskip}

\section{\texorpdfstring{{\tt SPEC}}{SPEC} (Species Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Species parameters ({\ct SPEC} namelist group)]{For more information see Section~\ref{info:SPEC}.}
\label{tbl:SPEC} \\
\hline
\multicolumn{5}{|c|}{{\ct SPEC} (Species Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct SPEC} (Species Parameters)} \\
\hline \hline
\endhead
{\ct AEROSOL}                       & Logical     & Section~\ref{info:deposition}           &                   & {\ct .FALSE.} \\ \hline
{\ct ALIAS}                         & Character   & Section~\ref{info:SPEC_advanced}        &                   &               \\ \hline
{\ct BACKGROUND}                    & Logical     & Section~\ref{info:SPEC}                 &                   & {\ct .FALSE.} \\ \hline
{\ct CONDUCTIVITY}                  & Real        & Section~\ref{gas_species_props}         & \si{W/(m.K)}      &               \\ \hline
{\ct CONDUCTIVITY\_SOLID}           & Real        & Section~\ref{info:deposition}           & \si{W/(m.K)}      &  0.26         \\ \hline
{\ct DENSITY\_LIQUID}               & Real        & Section~\ref{thermal_part_props}        & kg/m$^3$          &               \\ \hline
{\ct DENSITY\_SOLID}                & Real        & Section~\ref{info:deposition}           & kg/m$^3$          &  1800.        \\ \hline
{\ct DIFFUSIVITY}                   & Real        & Section~\ref{gas_species_props}         & m$^2$/s           &               \\ \hline
{\ct ENTHALPY\_OF\_FORMATION}       & Real        & Section~\ref{thermal_part_props}        & kJ/mol            &               \\ \hline
{\ct EPSILONKLJ}                    & Real        & Section~\ref{gas_species_props}         &                   & 0             \\ \hline
{\ct FIC\_CONCENTRATION}            & Real        & Section~\ref{info:FED}                  & ppm               & 0.            \\ \hline
{\ct FLD\_LETHAL\_DOSE}             & Real        & Section~\ref{info:FED}                  & ppm$\times$min    & 0.            \\ \hline
{\ct FORMULA }                      & Character   & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct HEAT\_OF\_VAPORIZATION}        & Real        & Section~\ref{thermal_part_props}        & kJ/kg             &               \\ \hline
{\ct H\_V\_REFERENCE\_TEMPERATURE}  & Real        & Section~\ref{thermal_part_props}        & $^\circ$C         &               \\ \hline
{\ct ID }                           & Character   & Section~\ref{info:SPEC_Basics}          &                   &               \\ \hline
{\ct LUMPED\_COMPONENT\_ONLY}       & Logical     & Section~\ref{info:lumped}               &                   & {\ct .FALSE.} \\ \hline
{\ct MASS\_EXTINCTION\_COEFFICIENT} & Real        & Section~\ref{info:alternative_smoke}    &                   & 0             \\ \hline
{\ct MASS\_FRACTION(:)}             & Real Array  & Section~\ref{info:lumped}               &                   & 0             \\ \hline
{\ct MASS\_FRACTION\_0}             & Real        & Section~\ref{info:SPEC_Basics}          &                   & 0             \\ \hline
{\ct MAX\_DIAMETER}                 & Real        & Section~\ref{info:agglomeration}        &    m              &               \\ \hline
{\ct MEAN\_DIAMETER}                & Real        & Section~\ref{info:deposition}           & m                 & 1.E-6         \\ \hline
{\ct MELTING\_TEMPERATURE}          & Real        & Section~\ref{thermal_part_props}        & $^\circ$C         &               \\ \hline
{\ct MIN\_DIAMETER}                 & Real        & Section~\ref{info:agglomeration}        & m                 &               \\ \hline
{\ct MW}                            & Real        & Section~\ref{gas_species_props}         & g/mol             & 29.           \\ \hline
{\ct N\_BINS}                       & Integer     & Section~\ref{info:agglomeration}        &                   &               \\ \hline
{\ct PR\_GAS}                       & Real        & Section~\ref{gas_species_props}         &                   & {\ct PR}      \\ \hline
{\ct PRIMITIVE}                     & Logical     & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct RADCAL\_ID}                    & Character   & Section~\ref{info:SPEC_advanced}        &                   &               \\ \hline
{\ct RAMP\_CP}                      & Character   & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct RAMP\_CP\_L}                   & Character   & Section~\ref{thermal_part_props}        &                   &               \\ \hline
{\ct RAMP\_D}                       & Character   & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct RAMP\_G\_F}                    & Character   & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct RAMP\_K}                       & Character   & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct RAMP\_MU}                      & Character   & Section~\ref{gas_species_props}         &                   &               \\ \hline
{\ct REFERENCE\_ENTHALPY}           & Real        & Section~\ref{gas_species_props}         & kJ/kg             &               \\ \hline
{\ct REFERENCE\_TEMPERATURE}        & Real        & Section~\ref{gas_species_props}         & $^\circ$C         & 25.           \\ \hline
{\ct SIGMALJ}                       & Real        & Section~\ref{gas_species_props}         &                   & 0             \\ \hline
{\ct SPEC\_ID(:)}                   & Character Array   & Section~\ref{info:lumped}             &                   &               \\ \hline
{\ct SPECIFIC\_HEAT}                & Real        & Section~\ref{gas_species_props}         & \si{kJ/(kg.K)}    &               \\ \hline
{\ct SPECIFIC\_HEAT\_LIQUID}        & Real        & Section~\ref{thermal_part_props}        & \si{kJ/(kg.K)}    &               \\ \hline
{\ct VAPORIZATION\_TEMPERATURE}     & Real        & Section~\ref{thermal_part_props}        & $^\circ$C         &               \\ \hline
{\ct VISCOSITY}                     & Real        & Section~\ref{gas_species_props}         & \si{kg/(m.s)}     &               \\ \hline
{\ct VOLUME\_FRACTION(:)}           & Real Array        & Section~\ref{info:lumped}             &                   &               \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt SURF}}{SURF} (Surface Properties)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Surface properties ({\ct SURF} namelist group)]{For more information see Section~\ref{info:SURF}.}
\label{tbl:SURF} \\
\hline
\multicolumn{5}{|c|}{{\ct SURF} (Surface Properties)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct SURF} (Surface Properties)} \\
\hline \hline
\endhead
{\ct ADIABATIC}                         & Logical         & Section~\ref{info:adiabatic}              &                     & {\ct .FALSE.}           \\ \hline
{\ct BACKING}                           & Character       & Section~\ref{info:BACKING}                &                     & {\ct 'EXPOSED'}         \\ \hline
{\ct BURN\_AWAY}                        & Logical         & Section~\ref{info:BURN_AWAY}              &                     & {\ct .FALSE.}           \\ \hline
{\ct CELL\_SIZE\_FACTOR}                & Real            & Section~\ref{info:solid_phase_stability}  &                     & 1.0                     \\ \hline
{\ct C\_FORCED\_CONSTANT}               & Real            & Section~\ref{info:convection}             &                     & 0.0                     \\ \hline
{\ct C\_FORCED\_PR\_EXP}                & Real            & Section~\ref{info:convection}             &                     & 0.0                     \\ \hline
{\ct C\_FORCED\_RE}                     & Real            & Section~\ref{info:convection}             &                     & 0.0                     \\ \hline
{\ct C\_FORCED\_RE\_EXP}                & Real            & Section~\ref{info:convection}             &                     & 0.0                     \\ \hline
{\ct C\_HORIZONTAL}                     & Real            & Section~\ref{info:convection}             &                     & 1.52                    \\ \hline
{\ct C\_VERTICAL}                       & Real            & Section~\ref{info:convection}             &                     & 1.31                    \\ \hline
{\ct COLOR    }                         & Character       & Section~\ref{info:colors}                 &                     &                         \\ \hline
{\ct CONVECTION\_LENGTH\_SCALE}         & Real            & Section~\ref{info:convection}             & m                   & 1.                      \\ \hline
{\ct CONVECTIVE\_HEAT\_FLUX}            & Real            & Section~\ref{info:convection}             & \si{kW/m^2}         &                         \\ \hline
{\ct CONVERT\_VOLUME\_TO\_MASS}         & Logical         & Section~\ref{info:MASS_FLUX}              &                     & {\ct .FALSE.}           \\ \hline
{\ct DEFAULT}                           & Logical         & Section~\ref{info:SURF}                   &                     & {\ct .FALSE.}           \\ \hline
{\ct DT\_INSERT}                        & Real            & Section~\ref{info:particle_flux}          & s                   & 0.01                    \\ \hline
{\ct EMISSIVITY}                        & Real            & Section~\ref{info:convection}             &                     & 0.9                     \\ \hline
{\ct EMISSIVITY\_BACK}                  & Real            & Section~\ref{info:BACKING}                &                     &                         \\ \hline
{\ct EVAC\_DEFAULT}                     & Logical         & Reference~\cite{FDS_Evac_Users_Guide}     &                     & {\ct .FALSE.}           \\ \hline
{\ct E\_COEFFICIENT}                    & Real            & Section~\ref{info:suppression}            & \si{m^2/(kg.s)}     &                         \\ \hline
{\ct EXTERNAL\_FLUX}                    & Real            & Section~\ref{solid_phase_verification}    & \si{kW/m^2}         &                         \\ \hline
{\ct EXTINCTION\_TEMPERATURE}           & Real            & Section~\ref{info:specified_burning}      & $^\circ$C           & -273.                   \\ \hline
{\ct FREE\_SLIP}                        & Logical         & Section~\ref{info:WALL_MODEL}             &                     & {\ct .FALSE.}           \\ \hline
{\ct GEOMETRY}                          & Character       & Section~\ref{info:GEOMETRY}               &                     & {\ct 'CARTESIAN'}       \\ \hline
{\ct HEAT\_OF\_VAPORIZATION}            & Real            & Section~\ref{info:specified_burning}      & kJ/kg               &                         \\ \hline
{\ct HEAT\_TRANSFER\_COEFFICIENT}       & Real            & Section~\ref{info:convection}             & \si{W/(m^2.K)}      &                         \\ \hline
{\ct \footnotesize
     HEAT\_TRANSFER\_COEFFICIENT\_BACK} & Real            & Section~\ref{info:convection}             & \si{W/(m^2.K)}      &                         \\ \hline
{\ct HEAT\_TRANSFER\_MODEL}             & Character       & Section~\ref{info:convection}             &                     &                         \\ \hline
{\ct HRRPUA}                            & Real            & Section~\ref{info:gas_burner}             & \si{kW/m^2}         &                         \\ \hline
{\ct HT3D}                              & Logical         & Section~\ref{info:ht3d}                   &                     & {\ct .FALSE.}           \\ \hline
{\ct ID}                                & Character       & Section~\ref{info:SURF}                   &                     &                         \\ \hline
{\ct IGNITION\_TEMPERATURE}             & Real            & Section~\ref{info:specified_burning}      & $^\circ$C           & 5000.                   \\ \hline
{\ct INNER\_RADIUS}                     & Real            & Section~\ref{info:PART_GEOMETRY}          & m                   &                         \\ \hline
{\ct INTERNAL\_HEAT\_SOURCE}            & Real Array      & Section~\ref{info:INTERNAL_HEAT_SOURCE}   & kW/m$^3$            &                         \\ \hline
{\ct LAYER\_DIVIDE}                     & Real            & Section~\ref{info:EXPOSED}                &                     & {\ct N\_LAYERS}/2       \\ \hline
{\ct LEAK\_PATH}                        & Int.~Pair       & Section~\ref{info:Leaks}                  &                     &                         \\ \hline
{\ct LENGTH}                            & Real            & Section~\ref{info:PART_GEOMETRY}          & m                   &                         \\ \hline
{\ct MASS\_FLUX(:)}                     & Real Array      & Section~\ref{info:MASS_FLUX}              & \si{kg/(m^2.s)}     &                         \\ \hline
{\ct MASS\_FLUX\_TOTAL}                 & Real            & Section~\ref{info:MASS_FLUX_TOTAL}        & \si{kg/(m^2.s)}     &                         \\ \hline
{\ct MASS\_FLUX\_VAR}                   & Real            & Section~\ref{info:MASS_FLUX_VAR}          &                     &                         \\ \hline
{\ct MASS\_FRACTION(:)}                 & Real Array      & Section~\ref{info:MASS_FLUX}              &                     &                         \\ \hline
{\ct MASS\_TRANSFER\_COEFFICIENT}       & Real            & Section~\ref{info:liquid_fuels}           & m/s                 &                         \\ \hline
{\ct MATL\_ID(NL,NC)}                   & Char.~Array     & Section~\ref{info:solid_pyrolysis}        &                     &                         \\ \hline
{\ct MATL\_MASS\_FRACTION(NL,NC)}       & Real Array      & Section~\ref{info:solid_pyrolysis}        &                     &                         \\ \hline
{\ct MINIMUM\_BURNOUT\_TIME}            & Real            & Section~\ref{veg_burnout_time}            & s                   & 1000000                 \\ \hline
{\ct MINIMUM\_LAYER\_THICKNESS}         & Real            & Section~\ref{info:solid_phase_stability}  & m                   & 1.E-6                   \\ \hline
{\ct MLRPUA }                           & Real            & Section~\ref{info:gas_burner}             & \si{kg/(m^2.s)}     &                         \\ \hline
{\ct MOISTURE\_FRACTION(:)}             & Real Array      & Section~\ref{info:vegetation}             &                     & 0.                      \\ \hline
{\ct N\_LAYER\_CELLS\_MAX}              & Integer Array   & Section~\ref{info:solid_phase_stability}  &                     & 1000                    \\ \hline
{\ct NET\_HEAT\_FLUX}                   & Real            & Section~\ref{info:convection}             & kW/m$^2$            &                         \\ \hline
{\ct NO\_SLIP}                          & Logical         & Section~\ref{info:WALL_MODEL}             &                     & {\ct .FALSE.}           \\ \hline
{\ct NPPC}                              & Integer         & Section~\ref{info:particle_flux}          &                     & 1                       \\ \hline
{\ct PACKING\_RATIO(:) }                & Real Array      & Section~\ref{pine_needles}                &                     &                         \\ \hline
{\ct PARTICLE\_MASS\_FLUX}              & Real            & Section~\ref{info:particle_flux}          & \si{kg/(m^2.s)}     &                         \\ \hline
{\ct PARTICLE\_SURFACE\_DENSITY}        & Real            & Section~\ref{info:particle_flux}          & kg/m$^2$            &                         \\ \hline
{\ct PART\_ID}                          & Character       & Section~\ref{info:particle_flux}          &                     &                         \\ \hline
{\ct PLE}                               & Real            & Section~\ref{info:stratification}         &                     & 0.3                     \\ \hline
{\ct PROFILE}                           & Character       & Section~\ref{info:profiles}               &                     &                         \\ \hline
{\ct RADIUS}                            & Real            & Section~\ref{info:PART_GEOMETRY}          & m                   &                         \\ \hline
{\ct RAMP\_EF}                          & Character       & Section~\ref{info:RAMP_Time}              &                     &                         \\ \hline
{\ct RAMP\_MF(:)}                       & Character       & Section~\ref{info:RAMP_Time}              &                     &                         \\ \hline
{\ct RAMP\_PART}                        & Character       & Section~\ref{info:RAMP_Time}              &                     &                         \\ \hline
{\ct RAMP\_Q}                           & Character       & Section~\ref{info:RAMP_Time}              &                     &                         \\ \hline
{\ct RAMP\_T}                           & Character       & Section~\ref{info:RAMP_Time}              &                     &                         \\ \hline
{\ct RAMP\_T\_B}                        & Character       & Section~\ref{info:TMP_INNER}              &                     &                         \\ \hline
{\ct RAMP\_T\_I}                        & Character       & Section~\ref{info:TMP_INNER}              &                     &                         \\ \hline
{\ct RAMP\_V}                           & Character       & Section~\ref{info:RAMP_Time}              &                     &                         \\ \hline
{\ct RAMP\_V\_X}                        & Character       & Section~\ref{info:RAMP_Vel_Prof}          &                     &                         \\ \hline
{\ct RAMP\_V\_Y}                        & Character       & Section~\ref{info:RAMP_Vel_Prof}          &                     &                         \\ \hline
{\ct RAMP\_V\_Z}                        & Character       & Section~\ref{info:RAMP_Vel_Prof}          &                     &                         \\ \hline
{\ct RGB(3)}                            & Int.~Triplet    & Section~\ref{info:colors}                 &                     & \small 255,204,102      \\ \hline
{\ct ROUGHNESS}                         & Real            & Section~\ref{info:WALL_MODEL}             & m                   & 0.                      \\ \hline
{\ct SPEC\_ID}                          & Character       & Section~\ref{info:MASS_FLUX}              &                     &                         \\ \hline
{\ct SPREAD\_RATE}                      & Real            & Section~\ref{info:spread}                 & m/s                 &                         \\ \hline
{\ct STRETCH\_FACTOR(:) }               & Real            & Section~\ref{info:solid_phase_stability}  &                     & 2.                      \\ \hline
{\ct SURFACE\_VOLUME\_RATIO(:) }        & Real            & Section~\ref{pine_needles}                & 1/m                 &                         \\ \hline
{\ct TAU\_EF}                           & Real            & Section~\ref{info:RAMP_Time}              & s                   & 1.                      \\ \hline
{\ct TAU\_MF(:)}                        & Real            & Section~\ref{info:RAMP_Time}              & s                   & 1.                      \\ \hline
{\ct TAU\_PART}                         & Real            & Section~\ref{info:RAMP_Time}              & s                   & 1.                      \\ \hline
{\ct TAU\_Q}                            & Real            & Section~\ref{info:RAMP_Time}              & s                   & 1.                      \\ \hline
{\ct TAU\_T}                            & Real            & Section~\ref{info:RAMP_Time}              & s                   & 1.                      \\ \hline
{\ct TAU\_V}                            & Real            & Section~\ref{info:RAMP_Time}              & s                   & 1.                      \\ \hline
{\ct TEXTURE\_HEIGHT}                   & Real            & Section~\ref{info:texture_map}            & m                   & 1.                      \\ \hline
{\ct TEXTURE\_MAP}                      & Character       & Section~\ref{info:texture_map}            &                     &                         \\ \hline
{\ct TEXTURE\_WIDTH}                    & Real            & Section~\ref{info:texture_map}            & m                   & 1.                      \\ \hline
{\ct TGA\_ANALYSIS}                     & Logical         & Section~\ref{info:TGA_DSC_MCC}            &                     & {\ct .FALSE.}           \\ \hline
{\ct TGA\_FINAL\_TEMPERATURE}           & Real            & Section~\ref{info:TGA_DSC_MCC}            & $^\circ$C           & 800.                    \\ \hline
{\ct TGA\_HEATING\_RATE}                & Real            & Section~\ref{info:TGA_DSC_MCC}            & $^\circ$C/min       & 5.                      \\ \hline
{\ct THICKNESS(NL)}                     & Real Array      & Section~\ref{info:SURF_MATL_Basics}       & m                   &                         \\ \hline
{\ct TMP\_BACK}                         & Real            & Section~\ref{info:TMP_INNER}              & $^\circ$C           & 20.                     \\ \hline
{\ct TMP\_FRONT}                        & Real            & Section~\ref{info:specified_temperature}  & $^\circ$C           & 20.                     \\ \hline
{\ct TMP\_INNER(:)}                     & Real Array      & Section~\ref{info:TMP_INNER}              & $^\circ$C           & 20.                     \\ \hline
{\ct TRANSPARENCY}                      & Real            & Section~\ref{info:colors}                 &                     & 1.                      \\ \hline
{\ct VEL    }                           & Real            & Section~\ref{info:Velocity_BC}            & m/s                 &                         \\ \hline
{\ct VEL\_BULK}                         & Real            & Section~\ref{info:profiles}               & m/s                 &                         \\ \hline
{\ct VEL\_GRAD}                         & Real            & Section~\ref{info:vel_grad}               & 1/s                 &                         \\ \hline
{\ct VEL\_T }                           & Real Pair       & Section~\ref{info:louvers}                & m/s                 &                         \\ \hline
{\ct VOLUME\_FLOW}                      & Real            & Section~\ref{info:Velocity_BC}            & \si{m^3/s}          &                         \\ \hline
{\ct WIDTH}                             & Real            & Section~\ref{info:PART_GEOMETRY}          & m                   &                         \\ \hline
{\ct XYZ(3)}                            & Real Triplet    & Section~\ref{info:spread}                 & m                   &                         \\ \hline
{\ct Z0 }                               & Real            & Section~\ref{info:stratification}         & m                   & 10.                     \\ \hline
\end{longtable}

% Undocumented: FIRELINE_MLR_MAX,N_CELLS_MAX
% VEGETATION, VEGETATION_ARRHENIUS_DEGRAD, VEGETATION_CDRAG, VEGETATION_CHAR_FRACTION,
% VEGETATION_ELEMENT_DENSITY, VEGETATION_GROUND_TEMP, VEGETATION_HEIGHT,
% VEGETATION_INITIAL_TEMP, VEGETATION_LAYERS, VEGETATION_LINEAR_DEGRAD, VEGETATION_LOAD,
% VEGETATION_LSET_IGNITE_TIME, VEGETATION_MOISTURE, VEGETATION_NO_BURN, VEGETATION_SVRATIO,
% VEG_LEVEL_SET_SPREAD, VEG_LSET_ROS_BACK, VEG_LSET_ROS_FLANK, VEG_LSET_ROS_HEAD,
% VEG_LSET_WIND_EXP

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt TABL}}{TABL} (Table Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Table parameters ({\ct TABL} namelist group)]{For more information see Section~\ref{info:spraypattern}.}
\label{tbl:TABL} \\
\hline
\multicolumn{5}{|c|}{{\ct TABL} (Table Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct TABL} (Table Parameters)} \\
\hline \hline
\endhead
{\ct ID}                & Character   & Section~\ref{info:spraypattern}      &             &     \\ \hline
{\ct TABLE\_DATA(9)}    & Real Array  & Section~\ref{info:spraypattern}      &             &     \\ \hline
\end{longtable}


\vspace{\baselineskip}


\section{\texorpdfstring{{\tt TIME}}{TIME} (Time Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Time parameters ({\ct TIME} namelist group)]{For more information see Section~\ref{info:TIME}.}
\label{tbl:TIME} \\
\hline
\multicolumn{5}{|c|}{{\ct TIME} (Time Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct TIME} (Time Parameters)} \\
\hline \hline
\endhead
{\ct DT}                        & Real       & Section~\ref{info:TIME_Control}           & s           &                 \\ \hline
{\ct EVAC\_DT\_FLOWFIELD}       & Real       & Reference~\cite{FDS_Evac_Users_Guide}     & s           &  0.01           \\ \hline
{\ct EVAC\_DT\_STEADY\_STATE}   & Real       & Reference~\cite{FDS_Evac_Users_Guide}     & s           &  0.05           \\ \hline
{\ct LIMITING\_DT\_RATIO}       & Real       & Section~\ref{info:Errors}                 &               &  0.0001         \\ \hline
{\ct LOCK\_TIME\_STEP}          & Logical    & Section~\ref{info:TIME_Control}           &             & {\ct .FALSE.}   \\ \hline
{\ct RESTRICT\_TIME\_STEP}      & Logical    & Section~\ref{info:TIME_Control}           &             & {\ct .TRUE.}    \\ \hline
{\ct T\_BEGIN}                  & Real       & Section~\ref{info:TIME_Basics}            & s           & 0.              \\ \hline
{\ct T\_END}                    & Real       & Section~\ref{info:TIME_Basics}            & s           & 1.              \\ \hline
{\ct TIME\_SHRINK\_FACTOR}      & Real       & Section~\ref{info:steady_state}           &             & 1.              \\ \hline
{\ct WALL\_INCREMENT}           & Integer    & Section~\ref{info:solid_phase_stability}  &             & 2               \\ \hline
\end{longtable}

\vspace{\baselineskip}

\section{\texorpdfstring{{\tt TRNX, TRNY, TRNZ}}{TRNX, TRNY, TRNZ} (MESH Transformations)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[MESH transformation parameters ({\ct TRN*} namelist groups)]{For more information see Section~\ref{info:TRNX}.}
\label{tbl:TRNX} \\
\hline
\multicolumn{5}{|c|}{{\ct TRNX, TRNY, TRNZ} (MESH Transformations)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct TRNX, TRNY, TRNZ} (MESH Transformations)} \\
\hline \hline
\endhead
{\ct CC    }            & Real          & Section~\ref{info:TRNX}   & m            &     \\ \hline
{\ct ID}                & Character     & Section~\ref{info:TRNX}   &              &     \\ \hline
{\ct IDERIV}            & Integer       & Section~\ref{info:TRNX}   &              &     \\ \hline
{\ct MESH\_NUMBER}      & Integer       & Section~\ref{info:TRNX}   &              &     \\ \hline
{\ct PC    }            & Real          & Section~\ref{info:TRNX}   &              &     \\ \hline
\end{longtable}

\vspace{\baselineskip}



\section{\texorpdfstring{{\tt VENT}}{VENT} (Vent Parameters)}


\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Vent parameters ({\ct VENT} namelist group)]{For more information see Section~\ref{info:VENT}.}
\label{tbl:VENT} \\
\hline
\multicolumn{5}{|c|}{{\ct VENT} (Vent Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct VENT} (Vent Parameters)} \\
\hline \hline
\endhead
{\ct COLOR    }             & Character         & Section~\ref{info:colors}                                 &               &                     \\ \hline
{\ct CTRL\_ID }             & Character         & Section~\ref{info:activate_deactivate}                    &               &                     \\ \hline
{\ct DEVC\_ID }             & Character         & Section~\ref{info:activate_deactivate}                    &               &                     \\ \hline
{\ct DYNAMIC\_PRESSURE}     & Real              & Section~\ref{info:pressure_boundary}                      & Pa            & 0.                  \\ \hline
{\ct EVACUATION    }        & Logical           & Reference~\cite{FDS_Evac_Users_Guide}                     &               &  {\ct .FALSE.}      \\ \hline
{\ct ID }                   & Character         & Section~\ref{info:VENT_Basics}                            &               &                     \\ \hline
{\ct IOR}                   & Integer           & Section~\ref{info:VENT_Trouble}                           &               &                     \\ \hline
{\ct L\_EDDY}               & Real              & Section~\ref{info:synthetic_turbulence}                   & m             & 0.                  \\ \hline
{\ct L\_EDDY\_IJ(3,3)}      & Real Array        & Section~\ref{info:synthetic_turbulence}                   & m             & 0.                  \\ \hline
{\ct MB    }                & Character         & Section~\ref{info:VENT_Basics}                            &               &                     \\ \hline
{\ct MESH\_ID    }          & Character         & Reference~\cite{FDS_Evac_Users_Guide}                     &               &                     \\ \hline
{\ct MULT\_ID    }          & Character         & Section~\ref{info:MULT}                                   &               &                     \\ \hline
{\ct N\_EDDY}               & Integer           & Section~\ref{info:synthetic_turbulence}                   &               & 0                   \\ \hline
{\ct OBST\_ID }             & Character         & Section~\ref{info:activate_deactivate}                    &               &                     \\ \hline
{\ct OUTLINE}               & Logical           & Section~\ref{info:VENT_Basics}                            &               &  {\ct .FALSE.}      \\ \hline
{\ct PBX, PBY, PBZ  }       & Real              & Section~\ref{info:VENT_Basics}                            &               &                     \\ \hline
{\ct PRESSURE\_RAMP}        & Character         & Section~\ref{info:pressure_boundary}                      &               &                     \\ \hline
{\ct REYNOLDS\_STRESS(3,3)} & Real Array        & Section~\ref{info:synthetic_turbulence}                   & m$^2$/s$^2$   & 0.                  \\ \hline
{\ct RGB(3)   }             & Integer Triplet   & Section~\ref{info:colors}                                 &               &                     \\ \hline
{\ct SPREAD\_RATE}          & Real              & Section~\ref{info:spread}                                 & m/s           &  0.05               \\ \hline
{\ct SURF\_ID}              & Character         & Section~\ref{info:VENT_Basics}                            &               &  {\ct 'INERT'}      \\ \hline
{\ct TEXTURE\_ORIGIN(3)}    & Real Triplet      & Section~\ref{info:texture_map}                            & m             & (0.,0.,0.)          \\ \hline
{\ct TMP\_EXTERIOR}         & Real              & Section~\ref{info:Special_VENTS}                          & $^\circ$C     &                     \\ \hline
{\ct TMP\_EXTERIOR\_RAMP}   & Character         & Section~\ref{info:Special_VENTS}                          &               &                     \\ \hline
{\ct TRANSPARENCY}          & Real              & Section~\ref{info:colors}                                 &               &   1.0               \\ \hline
{\ct UVW(3) }               & Real Triplet      & Section~\ref{info:HVAClouvers}                            &               &                     \\ \hline
{\ct VEL\_RMS}              & Real              & Section~\ref{info:synthetic_turbulence}                   & m/s           & 0.                  \\ \hline
{\ct XB(6) }                & Real Sextuplet    & Section~\ref{info:VENT_Basics}                            & m             &                     \\ \hline
{\ct XYZ(3) }               & Real Triplet      & Section~\ref{info:spread}                                 & m             &                     \\ \hline
\end{longtable}


\vspace{\baselineskip}



\section{\texorpdfstring{{\tt WIND}}{WIND} (Wind and Atmospheric Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Wind and atmospheric parameters ({\ct WIND} namelist group)]{For more information see Section~\ref{info:WIND}.}
\label{tbl:WIND} \\
\hline
\multicolumn{5}{|c|}{{\ct WIND} (Wind and atmospheric parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct WIND} (Wind and atmospheric parameters)} \\
\hline \hline
\endhead
{\ct CORIOLIS\_VECTOR(3)}                       & Real          & Section~\ref{info:coriolis_force}             &               & 0.                \\ \hline
{\ct DIRECTION}                                 & Real          & Section~\ref{info:WIND}                       & degrees       & 270               \\ \hline
{\ct DT\_MEAN\_FORCING}                         & Real          & Section~\ref{info:WIND}                       & s             & 1.                \\ \hline
{\ct FORCE\_VECTOR(3)}                          & Real          & Section~\ref{info:force_vector}               &               & 0.                \\ \hline
{\ct GEOSTROPHIC\_WIND(2)}                      & Real          & Section~\ref{info:geostrophic_wind}           & m/s           &                   \\ \hline
{\ct GROUND\_LEVEL}                             & Real          & Section~\ref{info:stratification}             & m             & 0.                \\ \hline
{\ct L}                                         & Real          & Section~\ref{info:WIND}                       & m             & 0                 \\ \hline
{\ct LAPSE\_RATE}                               & Real          & Section~\ref{info:stratification}             & $^\circ$C/m   & 0                 \\ \hline
{\ct LATITUDE}                                  & Real          & Section~\ref{info:coriolis_force}             & degrees       &                   \\ \hline
{\ct RAMP\_DIRECTION}                           & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_FVX\_T}                              & Character     & Section~\ref{info:force_vector}               &               &                   \\ \hline
{\ct RAMP\_FVY\_T}                              & Character     & Section~\ref{info:force_vector}               &               &                   \\ \hline
{\ct RAMP\_FVZ\_T}                              & Character     & Section~\ref{info:force_vector}               &               &                   \\ \hline
{\ct RAMP\_SPEED}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_TMP0\_Z}                             & Character     & Section~\ref{info:stratification}             &               &                   \\ \hline
{\ct RAMP\_U0\_T}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_V0\_T}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_W0\_T}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_U0\_Z}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_V0\_Z}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct RAMP\_W0\_Z}                               & Character     & Section~\ref{info:WIND}                       &               &                   \\ \hline
{\ct SPONGE\_CELLS}                             & Integer       & Section~\ref{info:SPONGE_CELLS}               &               & 3                 \\ \hline
{\ct SPEED}                                     & Real          & Section~\ref{info:WIND}                       & m/s           & 0.                \\ \hline
{\ct STRATIFICATION}                            & Logical       & Section~\ref{info:stratification}             &               & {\ct .TRUE.}      \\ \hline
{\ct THETA\_STAR}                               & Real          & Section~\ref{info:WIND}                       & K             &                   \\ \hline
{\ct U0,V0,W0}                                  & Reals         & Section~\ref{info:WIND}                       & m/s           & 0.                \\ \hline
{\ct U\_STAR}                                   & Real          & Section~\ref{info:WIND}                       & m/s           &                   \\ \hline
%{\ct USE_ATMOSPHERIC_INTERPOLATION}             & Logical       & Flux match TMP for atmospheric flows          &               & {\ct .FALSE.}      \\ \hline
{\ct Z\_0}                                      & Real          & Section~\ref{info:WIND}                       & m             & 0.03              \\ \hline
{\ct Z\_REF}                                    & Real          & Section~\ref{info:WIND}                       & m             & 2.                \\ \hline
\end{longtable}

\vspace{\baselineskip}


\section{\texorpdfstring{{\tt ZONE}}{ZONE} (Pressure Zone Parameters)}

\begin{longtable}{@{\extracolsep{\fill}}|l|l|l|l|l|}
\caption[Pressure zone parameters ({\ct ZONE} namelist group)]{For more information see Section~\ref{info:ZONE}.}
\label{tbl:ZONE} \\
\hline
\multicolumn{5}{|c|}{{\ct ZONE} (Pressure Zone Parameters)} \\
\hline \hline
\endfirsthead
\caption[]{Continued} \\
\hline
\multicolumn{5}{|c|}{{\ct ZONE} (Pressure Zone Parameters)} \\
\hline \hline
\endhead
{\ct ID}                           & Character             & Section~\ref{info:ZONE_Basics}     &        &               \\ \hline
{\ct LEAK\_AREA(N)}                & Real                  & Section~\ref{info:Leaks}           & m$^2$  & 0             \\ \hline
{\ct LEAK\_PRESSURE\_EXPONENT(N)}  & Real                  & Section~\ref{info:Leaks}           &        & 0.5           \\ \hline
{\ct LEAK\_REFERENCE\_PRESSURE(N)} & Real                  & Section~\ref{info:Leaks}           & Pa     & 4             \\ \hline
{\ct PERIODIC}                     & Logical               & Section~\ref{info:ZONE_Basics}     &        & {\ct .FALSE.} \\ \hline
{\ct XB(6)}                        & Real Sextuplet        & Section~\ref{info:ZONE_Basics}     & m      &               \\ \hline
{\ct XYZ(3:N)}                     & Real Triplet Array    & Section~\ref{info:ZONE_Basics}     & m      &               \\ \hline
\end{longtable}

\part{FDS and Smokeview Development Tools}

\chapter{The FDS and Smokeview Repositories}

For those interested in obtaining the FDS and Smokeview source codes, either for development work or simply to compile on a particular platform, it is strongly suggested that you download onto your computer the FDS and Smokeview repositories. All project documents are maintained using the online utility \href{https://github.com/}{{GitHub}}, a free service that supports software development for open source applications.  GitHub uses Git version control software. Under this system, a centralized repository containing all project files resides on a GitHub server.  Anyone can obtain a copy of the repository or retrieve a specific revision of the repository.  However, only the FDS and Smokeview developers can commit changes directly to the repository. Others must submit a ``pull request.'' Detailed instructions for checking out the FDS repository can be found at
\href{https://github.com/firemodels/fds}{{https://github.com/firemodels/fds}}.

Both FDS and Smokeview live within a GitHub \emph{organization} called ``firemodels''.  The current location of the organization is \href{https://github.com/firemodels}{{https://github.com/firemodels}}.  The repositories that are used by the FDS and Smokeview projects are listed below along with a brief description:

\vskip\baselineskip
\begin{tabular}{ll}
fds & FDS source code, verification and validation tests, wikis, and documentation \\
smv & Smokeview source code, integration tests, and documentation \\
exp & Experimental data repository for FDS validation \\
out & FDS output results for validation \\
bot & Firebot (continuous integration system) source \\
fds-smv & Web page html source
\end{tabular}
\vskip\baselineskip

\noindent The wiki pages in the fds repository are particularly useful in describing the details of how you go about working with the repository assets.

"""

FDS_MANUAL_TABLE_GROUP_NAMELIST = r"""
Table~\ref{tbl:namelistgroups} provides a quick reference to all the namelist parameters and where you can find the reference to where it is introduced in the document and the table containing all of the keywords for each group.

\vspace{\baselineskip}
\begin{table}[ht]
\begin{center}
\caption{Namelist Group Reference Table}
\label{tbl:namelistgroups}
\begin{tabular}{|c|l|c|c|}
\hline
Group Name  & Namelist Group Description   & Reference Section & Parameter Table  \\ \hline
{\ct BNDF}  & Boundary File Output         & \ref{info:BNDF} & \ref{tbl:BNDF}  \\ \hline
{\ct CATF}  & Concatenate Input Files      & \ref{info:CATF} & \ref{tbl:CATF}  \\ \hline
{\ct CLIP}  & Clipping Parameters          & \ref{info:CLIP} & \ref{tbl:CLIP}  \\ \hline
{\ct COMB}  & Combustion Parameters        & \ref{info:COMB} & \ref{tbl:COMB}  \\ \hline
{\ct CSVF}  & Velocity Input File          & \ref{info:CSVF} & \ref{tbl:CSVF}  \\ \hline
{\ct CTRL}  & Control Function Parameters  & \ref{info:CTRL} & \ref{tbl:CTRL}  \\ \hline
{\ct DEVC}  & Device Parameters            & \ref{info:DEVC} & \ref{tbl:DEVC}  \\ \hline
{\ct DUMP}  & Output Parameters            & \ref{info:DUMP} & \ref{tbl:DUMP}  \\ \hline
{\ct HEAD}  & Input File Header            & \ref{info:HEAD} & \ref{tbl:HEAD}  \\ \hline
{\ct HOLE}  & Obstruction Cutout           & \ref{info:HOLE} & \ref{tbl:HOLE}  \\ \hline
{\ct HVAC}  & Heating, Vent., Air Cond.    & \ref{info:HVAC} & \ref{tbl:HVAC}  \\ \hline
{\ct INIT}  & Initial Condition            & \ref{info:INIT} & \ref{tbl:INIT}  \\ \hline
{\ct ISOF}  & Isosurface File Output       & \ref{info:ISOF} & \ref{tbl:ISOF}  \\ \hline
{\ct MATL}  & Material Property            & \ref{info:MATL} & \ref{tbl:MATL}  \\ \hline
{\ct MESH}  & Mesh Parameters              & \ref{info:MESH} & \ref{tbl:MESH}  \\ \hline
{\ct MISC}  & Miscellaneous                & \ref{info:MISC} & \ref{tbl:MISC}  \\ \hline
{\ct MOVE}  & Transformation Parameters    & \ref{info:MOVE} & \ref{tbl:MOVE}  \\ \hline
{\ct MULT}  & Multiplier Parameters        & \ref{info:MULT} & \ref{tbl:MULT}  \\ \hline
{\ct OBST}  & Obstruction                  & \ref{info:OBST} & \ref{tbl:OBST}  \\ \hline
{\ct PART}  & Lagrangian Particle          & \ref{info:PART} & \ref{tbl:PART}  \\ \hline
{\ct PRES}  & Pressure Solver Parameters   & \ref{info:PRES} & \ref{tbl:PRES}  \\ \hline
{\ct PROF}  & Profile Output               & \ref{info:PROF} & \ref{tbl:PROF}  \\ \hline
{\ct PROP}  & Device Property              & \ref{info:PROP} & \ref{tbl:PROP}  \\ \hline
{\ct RADF}  & Radiation Output File        & \ref{info:RADF} & \ref{tbl:RADF}  \\ \hline
{\ct RADI}  & Radiation                    & \ref{info:RADI} & \ref{tbl:RADI}  \\ \hline
{\ct RAMP}  & Ramp Profile                 & \ref{info:RAMP} & \ref{tbl:RAMP}  \\ \hline
{\ct REAC}  & Reaction Parameters          & \ref{info:REAC} & \ref{tbl:REAC}  \\ \hline
{\ct SLCF}  & Slice File Output            & \ref{info:SLCF} & \ref{tbl:SLCF}  \\ \hline
{\ct SPEC}  & Species Parameters           & \ref{info:SPEC} & \ref{tbl:SPEC}  \\ \hline
{\ct SURF}  & Surface Properties           & \ref{info:SURF} & \ref{tbl:SURF}  \\ \hline
{\ct TABL}  & Tabulated Particle Data      & \ref{info:TABL} & \ref{tbl:TABL}  \\ \hline
{\ct TIME}  & Simulation Time              & \ref{info:TIME} & \ref{tbl:TIME}  \\ \hline
{\ct TRNX}  & Mesh Stretching              & \ref{info:TRNX} & \ref{tbl:TRNX}  \\ \hline
{\ct VENT}  & Vent Parameters              & \ref{info:VENT} & \ref{tbl:VENT}  \\ \hline
{\ct WIND}  & Wind Parameters              & \ref{info:WIND} & \ref{tbl:WIND}  \\ \hline
{\ct ZONE}  & Pressure Zone Parameters     & \ref{info:ZONE} & \ref{tbl:ZONE}  \\ \hline
\end{tabular}
\end{center}
\end{table}

"""


class FDS2Dict:
    pass


def all_fds_groups_in_a_list(fds_manual_latex: str = None):
    # Parse input, i.e. the manual latex source code
    # ==============================================
    if fds_manual_latex is None:
        out = FDS_MANUAL_TABLE_GROUP_NAMELIST
    else:
        out = fds_manual_latex

    # Analyse the source code, extract FDS input parameters
    # =====================================================

    # replace all escaped characters
    out = out.replace("\\", "")
    # remove all commented-out lines
    out = re.sub(r"%[\s\S.]*?[\r|\n]", "", out)
    # remove multiple \n or \r, step 1 - split string
    out = re.split(r"[\r|\n]", out)
    # remove multiple \n or \r, step 2 - remove empty lines
    out = list(filter(None, out))
    # remove multiple \n or \r, step 3 - restore to a single string
    out = "\n".join(out)
    # find all possible FDS input parameters
    out = re.findall(r"\n{ct\s([\w]*)[(\}]", out)
    # filter out duplicated and sort all the items
    out = sorted(list(set(out)))

    return out


def all_fds_input_parameters_in_a_list(fds_manual_latex: str = None):
    """Get an exhausted list of input parameters for all groups in Fire Dynamics Simulator.

    :param fds_manual_latex: text string in latex source code obtained from FDS manual source codes.
    :return: a list of all input parameters extracted from the supplied FDS manual latex source code.
    """

    # Parse input, i.e. the manual latex source code
    # ==============================================

    if fds_manual_latex is None:
        fds_manual_latex = FDS_MANUAL_CHAPTER_LIST_OF_INPUT_PARAMETERS
    else:
        fds_manual_latex = fds_manual_latex

    # remove latex formatter
    fds_manual_latex = re.sub(r"\\footnotesize *[\n\r]*?", " ", fds_manual_latex)

    # Analyse the source code, extract FDS input parameters
    # =====================================================

    # replace all escaped characters
    fds_manual_latex = fds_manual_latex.replace("\\", "")
    # remove all commented-fds_manual_latex lines
    fds_manual_latex = re.sub(r"%[\s\S.]*?[\r\n]", "", fds_manual_latex)
    # remove multiple \n or \r, step 1 - split string
    fds_manual_latex = re.split(r"[\r\n]", fds_manual_latex)
    # remove multiple \n or \r, step 2 - remove empty lines
    fds_manual_latex = list(filter(None, fds_manual_latex))
    # remove multiple \n or \r, step 3 - restore to a single string
    fds_manual_latex = "\n".join(fds_manual_latex)
    # find all possible FDS input parameters
    fds_manual_latex = re.findall(r"\n{ct\s([\w]+)[(\} *,]", fds_manual_latex) + [
        "PBY",
        "PBZ",
        "FYI",
    ]
    # filter fds_manual_latex duplicated and sort all the items
    fds_manual_latex = sorted(list(set(fds_manual_latex)))

    return fds_manual_latex
