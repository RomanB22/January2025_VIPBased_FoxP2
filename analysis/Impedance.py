import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D  # Import for 3D plotting

# Define a consistent color palette for conditions
CONDITION_COLORS = {
    'InVivo_Go': 'blue',
    'MirrorDecre_Go': 'green',
    'Other_Condition': 'red'  # Add more conditions and colors as needed
}

def process_json_files(json_dir='data/'):
    """
    Process JSON files and store results in a dictionary.
    """
    # Get a list of JSON files in the directory
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]

    # Dictionary to store results
    results = []

    # Process each JSON file
    for i, file_path in enumerate(json_files[:50]):
        try:
            print(f'****************** Processing file: {i+1}/{len(json_files)}')
            # Load the JSON file
            with open(file_path, 'r') as f:
                file = json.load(f)

            # Extract IncreConn, DecreConn, and Condition
            incre = file['simConfig']['IncreConn']
            decre = file['simConfig']['DecreConn']
            condition = file['simConfig']['Condition']

            # Extract impedance data
            impedance_data = file['simData']['Impedance']

            # Extract times and impedances
            times = np.array(list(map(float, impedance_data.keys())))  # Convert times to float
            impedances = np.array(list(impedance_data.values()))  # List of impedance values

            # Store results in the dictionary
            results.append({
                'incre': incre,
                'decre': decre,
                'ratio':incre/(incre+decre),
                'condition': condition,
                'times': times,
                'impedances': impedances,  # Include raw impedance data
                'avg_curve': np.mean(impedances, axis=1)  # Compute the average at each time point
            })

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return results


def plot_grouped_curves(results, output_dir='data/avg_curves'):
    """
    Plot curves with the same incre and decre in the same figure, including error bands.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Group results by (incre, decre)
    grouped_results = defaultdict(list)
    for result in results:
        key = (result['incre'], result['decre'])
        grouped_results[key].append(result)

    # Plot each group
    for (incre, decre), group in grouped_results.items():
        plt.figure(figsize=(10, 6))

        # Calculate the average curve and confidence interval for each condition
        for result in group:
            times = result['times']
            avg_curve = result['avg_curve']
            std_dev = np.std(result['avg_curve'], axis=0)  # Standard deviation
            n = len(result['avg_curve'])  # Number of samples
            confidence_interval = 1.96 * (std_dev / np.sqrt(n))  # 95% confidence interval

            # Plot the average curve
            plt.plot(times, avg_curve, marker='o', linestyle='-', 
                     label=f"Condition={result['condition']}", 
                     color=CONDITION_COLORS.get(result['condition'], 'black'))

            # Plot the error band
            plt.fill_between(times, 
                             avg_curve - confidence_interval, 
                             avg_curve + confidence_interval, 
                             alpha=0.3, 
                             color=CONDITION_COLORS.get(result['condition'], 'black'))

        # Customizing the plot
        plt.xlabel('Time')
        plt.ylabel('Impedance (Ohms)')
        plt.title(f'Average Impedance (Incre={incre}, Decre={decre})')
        plt.legend(loc='best')
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.xlim(1000, 2500)

        # Save the plot
        output_file = os.path.join(output_dir, f'average_impedance_incre_{incre}_decre_{decre}.png')
        plt.savefig(output_file)
        plt.close()  # Close the figure to free up memory

        print(f"Plot saved to {output_file}")

def plot_grouped_curves_by_ratio(results, output_dir='data/avg_curves_grouped_by_ratio'):
    """
    Group impedances by ratio and condition, stack trials, calculate mean, std, and 95% CI, and plot the results.
    Curves with the same ratio but different conditions are plotted on the same figure.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dictionary to store grouped data by ratio
    grouped_data_by_ratio = {}

    # Group data by ratio and then by condition
    for result in results:
        ratio = result['ratio']
        condition = result['condition']
        if ratio not in grouped_data_by_ratio:
            grouped_data_by_ratio[ratio] = {}
        if condition not in grouped_data_by_ratio[ratio]:
            grouped_data_by_ratio[ratio][condition] = {
                'times': result['times'],
                'impedances': []
            }
        grouped_data_by_ratio[ratio][condition]['impedances'].append(result['impedances'])

    # Process each ratio group
    for ratio, conditions_data in grouped_data_by_ratio.items():
        plt.figure(figsize=(10, 6))
        for condition, data in conditions_data.items():
            times = data['times']
            impedances_stacked = np.hstack(data['impedances'])  # Stack trials vertically (one trial per row)

            # Calculate mean and std along axis=1 (across trials for each time point)
            mean_impedance = np.mean(impedances_stacked, axis=1)  # Mean across trials (axis=0)
            std_impedance = np.std(impedances_stacked, axis=1)    # Std across trials (axis=0)
            n = impedances_stacked.shape[0]  # Number of trials
            ci = 1.96 * (std_impedance / np.sqrt(n))  # 95% confidence interval

            # Plot the results for this condition
            plt.plot(times, mean_impedance, label=f'Condition: {condition}')
            plt.fill_between(times, mean_impedance - ci, mean_impedance + ci, alpha=0.2)

        # Add labels, title, legend, and grid for the figure
        plt.xlabel('Time')
        plt.ylabel('Impedance')
        plt.title(f'Impedance vs Time (Ratio: {ratio:.2f})')
        plt.legend()
        plt.grid(True)

        # Save the figure
        filename = f'{output_dir}/impedance_ratio_{ratio:.2f}.png'
        plt.savefig(filename)
        plt.close()

def create_boxplots(results, output_dir='data/boxplots'):
    """
    Create separate boxplots for the mean impedances before and after the cue (1800 ms) for each condition.
    The x-axis represents the ratio increconn / (increconn + decreconn),
    and the legend represents the total (increconn + decreconn).
    """
    os.makedirs(output_dir, exist_ok=True)
    cue_time = 1800
    points = int(cue_time / 100)  # Assuming 100 ms intervals

    # Lists to store the data
    impedance_data = []

    # Process each file
    for file in results:
        ratio = file['incre'] / (file['incre'] + file['decre'])
        total_conn = file['incre'] + file['decre']
        condition = file['condition']
        
        mean_pre_cue = np.mean(file['impedances'][:points], axis=0)
        mean_post_cue = np.mean(file['impedances'][points:], axis=0)

        for i in range(len(mean_pre_cue)):
            impedance_data.append({
                'condition': condition,
                'ratio': ratio,
                'total_conn': total_conn,
                'mean_impedance': mean_pre_cue[i],
                'time_period': 'Pre-Cue'
            })
            impedance_data.append({
                'condition': condition,
                'ratio': ratio,
                'total_conn': total_conn,
                'mean_impedance': mean_post_cue[i],
                'time_period': 'Post-Cue'
            })

    # Convert to DataFrame
    df = pd.DataFrame(impedance_data)

    # Plot separate boxplots for pre-cue and post-cue
    for time_period in ['Pre-Cue', 'Post-Cue']:
        plt.figure(figsize=(12, 8))
        df_period = df[df['time_period'] == time_period]
        sns.boxplot(data=df_period, x='ratio', y='mean_impedance', hue='total_conn')
        plt.title(f'Mean Impedance ({time_period})')
        plt.xlabel('Ratio (IncreConn / (IncreConn + DecreConn))')
        plt.ylabel('Mean Impedance')
        plt.legend(title='Total Connections')
        
        output_file = os.path.join(output_dir, f'boxplot_{time_period.lower()}.png')
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Plot saved to {output_file}')
        
def plot_3d_per_condition(results, output_dir='data/3d_plots_per_condition', use_surface=False):
    """
    Create a 3D plot of impedance vs. time vs. ratio for each condition.
    If use_surface is True, plot as a surface; otherwise, plot as lines.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Group results by condition
    grouped_results = defaultdict(list)
    for result in results:
        grouped_results[result['condition']].append(result)

    # Create a 3D plot for each condition
    for condition, group in grouped_results.items():
        # Prepare data for the 3D plot
        times = group[0]['times']  # All results have the same times
        ratios = []
        avg_curves = []

        for result in group:
            ratio = result['incre'] / (result['incre'] + result['decre'])
            ratios.append(ratio)
            avg_curves.append(result['avg_curve'])

        # Convert to numpy arrays
        ratios = np.array(ratios)
        avg_curves = np.array(avg_curves)

        # Create the 3D plot
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        if use_surface:
            # Create a meshgrid for time and ratio
            time_grid, ratio_grid = np.meshgrid(times, ratios)

            # Plot the surface
            surf = ax.plot_surface(time_grid, ratio_grid, avg_curves, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)  # Add a color bar
        else:
            # Plot lines for each ratio
            for i, ratio in enumerate(ratios):
                ax.plot(times, np.full_like(times, ratio), avg_curves[i], 
                         label=f'Ratio={ratio:.2f}')
       

        # Customizing the plot
        ax.set_xlabel('Time')
        ax.set_ylabel('Ratio (Incre / (Incre + Decre))')
        ax.set_zlabel('Impedance (Ohms)')
        ax.set_title(f'3D Plot of Impedance vs. Time vs. Ratio (Condition: {condition})')

        # Save the plot
        plot_type = 'surface' if use_surface else 'lines'
        output_file = os.path.join(output_dir, f'3d_impedance_vs_time_vs_ratio_condition_{condition}_{plot_type}.png')
        plt.savefig(output_file)
        plt.close()  # Close the figure to free up memory

        print(f"3D plot for condition '{condition}' saved to {output_file}")

def create_violinplots(results, output_dir='data/violinplots'):
    """
    Create violin plots comparing InVivo_Go and MirrorDecre_Go conditions.
    One side of the violin represents InVivo_Go, and the other side represents MirrorDecre_Go.
    """
    os.makedirs(output_dir, exist_ok=True)
    cue_time = 1800
    points = int(cue_time / 100)

    impedance_data = []

    for file in results:
        ratio = file['incre'] / (file['incre'] + file['decre'])
        total_conn = file['incre'] + file['decre']
        condition = file['condition']

        if condition in ['InVivo_Go', 'MirrorDecre_Go']:
            mean_pre_cue = np.mean(file['impedances'][:points], axis=0)
            mean_post_cue = np.mean(file['impedances'][points:], axis=0)

            for i in range(len(mean_pre_cue)):
                impedance_data.append({
                    'condition': condition,
                    'ratio': ratio,
                    'total_conn': total_conn,
                    'mean_impedance': mean_pre_cue[i],
                    'time_period': 'Pre-Cue'
                })
                impedance_data.append({
                    'condition': condition,
                    'ratio': ratio,
                    'total_conn': total_conn,
                    'mean_impedance': mean_post_cue[i],
                    'time_period': 'Post-Cue'
                })

    df = pd.DataFrame(impedance_data)

    plt.figure(figsize=(12, 8))
    sns.violinplot(data=df, x='ratio', y='mean_impedance', hue='condition', split=True, inner='quartile')
    plt.title('Violin Plot of Mean Impedance: InVivo_Go vs. MirrorDecre_Go')
    plt.xlabel('Ratio (IncreConn / (IncreConn + DecreConn))')
    plt.ylabel('Mean Impedance')
    plt.legend(title='Condition')

    output_file = os.path.join(output_dir, 'violinplot_InVivo_vs_MirrorDecre.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()
    print(f'Plot saved to {output_file}')

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_boxplots_total_connections(results, output_dir='data/boxplots_total_connections'):
    """
    Create separate boxplots for the mean impedances before and after the cue (1800 ms) for each condition.
    The x-axis represents the total number of connections (incre + decre),
    and the legend represents the condition.
    """
    os.makedirs(output_dir, exist_ok=True)
    cue_time = 1800
    points = int(cue_time / 100)  # Assuming 100 ms intervals

    impedance_data_pre = []
    impedance_data_post = []

    for file in results:
        # Validate necessary keys
        if not all(key in file for key in ['incre', 'decre', 'condition', 'impedances']):
            print(f"Skipping file due to missing keys: {file.keys()}")
            continue
        
        total_conn = file['incre'] + file['decre']
        condition = file['condition']
        impedances = np.array(file['impedances'])

        if len(impedances) < points:  # Handle short impedance arrays
            print(f"Skipping file due to insufficient impedance data: {len(impedances)} < {points}")
            continue

        mean_pre_cue = np.mean(impedances[:points], axis=0)
        mean_post_cue = np.mean(impedances[points:], axis=0)

        for i in range(len(mean_pre_cue)):
            impedance_data_pre.append({
                'condition': condition,
                'total_conn': total_conn,
                'mean_impedance': mean_pre_cue[i]
            })
            impedance_data_post.append({
                'condition': condition,
                'total_conn': total_conn,
                'mean_impedance': mean_post_cue[i]
            })

    # Convert to DataFrames
    df_pre = pd.DataFrame(impedance_data_pre)
    df_post = pd.DataFrame(impedance_data_post)

    # Function to create and save a boxplot
    def plot_and_save(df, time_period, filename):
        if df.empty:
            print(f"No valid data to plot for {time_period}.")
            return
        
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=df, x='total_conn', y='mean_impedance', hue='condition', 
                    order=sorted(df['total_conn'].unique()))
        plt.title(f'Mean Impedance by Total Connections ({time_period})')
        plt.xlabel('Total Connections (Incre + Decre)')
        plt.ylabel('Mean Impedance')
        plt.legend(title='Condition')
        plt.xticks(rotation=45)

        output_file = os.path.join(output_dir, filename)
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Plot saved to {output_file}')

    # Generate separate plots
    plot_and_save(df_pre, "Pre-Cue", 'boxplot_total_connections_pre.png')
    plot_and_save(df_post, "Post-Cue", 'boxplot_total_connections_post.png')

def create_violinplots_total_connections(results, output_dir='data/violinplots_total_connections'):
    """
    Create separate violin plots comparing InVivo_Go and MirrorDecre_Go conditions.
    The x-axis represents the total number of connections (incre + decre),
    and the legend represents the condition.
    """
    os.makedirs(output_dir, exist_ok=True)
    cue_time = 1800
    points = int(cue_time / 100)  # Assuming 100 ms intervals

    impedance_data_pre = []
    impedance_data_post = []

    for file in results:
        # Validate necessary keys
        if not all(key in file for key in ['incre', 'decre', 'condition', 'impedances']):
            print(f"Skipping file due to missing keys: {file.keys()}")
            continue
        
        total_conn = file['incre'] + file['decre']
        condition = file['condition']

        if condition in ['InVivo_Go', 'MirrorDecre_Go']:
            impedances = np.array(file['impedances'])

            if len(impedances) < points:  # Handle short impedance arrays
                print(f"Skipping file due to insufficient impedance data: {len(impedances)} < {points}")
                continue

            mean_pre_cue = np.mean(impedances[:points], axis=0)
            mean_post_cue = np.mean(impedances[points:], axis=0)

            for i in range(len(mean_pre_cue)):
                impedance_data_pre.append({
                    'condition': condition,
                    'total_conn': total_conn,
                    'mean_impedance': mean_pre_cue[i]
                })
                impedance_data_post.append({
                    'condition': condition,
                    'total_conn': total_conn,
                    'mean_impedance': mean_post_cue[i]
                })

    # Convert to DataFrames
    df_pre = pd.DataFrame(impedance_data_pre)
    df_post = pd.DataFrame(impedance_data_post)

    # Function to create and save a violin plot
    def plot_and_save(df, time_period, filename):
        if df.empty:
            print(f"No valid data to plot for {time_period}.")
            return
        
        plt.figure(figsize=(12, 8))
        sns.violinplot(data=df, x='total_conn', y='mean_impedance', hue='condition', 
                       split=True, inner='quartile', order=sorted(df['total_conn'].unique()))
        plt.title(f'Violin Plot of Mean Impedance by Total Connections ({time_period})')
        plt.xlabel('Total Connections (Incre + Decre)')
        plt.ylabel('Mean Impedance')
        plt.legend(title='Condition')
        plt.xticks(rotation=45)

        output_file = os.path.join(output_dir, filename)
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Plot saved to {output_file}')

    # Generate separate plots
    plot_and_save(df_pre, "Pre-Cue", 'violinplot_total_connections_pre.png')
    plot_and_save(df_post, "Post-Cue", 'violinplot_total_connections_post.png')

# Main execution
if __name__ == "__main__":
    # Process JSON files and store results
    folder = "data/gridsearch_DepFalse_sim"
    results = process_json_files(folder)

    # Plot grouped curves by (incre, decre)
    plot_grouped_curves(results)

    # Plot grouped curves by ratio incre / (incre + decre)
    plot_grouped_curves_by_ratio(results)

    # Plot 3D impedance vs. time vs. ratio for each condition
    plot_3d_per_condition(results, use_surface=True)

    # Plot boxplots with a maximum of 5 boxplots per figure
    create_boxplots(results)

    # Plot violin plots with a maximum of 5 violin plots per figure
    create_violinplots(results)

    # Plot boxplots for total connections
    create_boxplots_total_connections(results)

    # Plot violin plots for total connections
    create_violinplots_total_connections(results)