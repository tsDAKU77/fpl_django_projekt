from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Player, Squad, XI
from .forms import LoginRegisterForm
import chardet
import pandas as pd

# Path to the Excel file

# Path to the CSV file
EXCEL_FILE_PATH = r"H:\TEJAS\ProgPrac\.Py\PROJEKT\django\FPL\FL_sheet.csv"

def player_stats(request):
    """View for users to read, sort, and filter the existing CSV file."""
    # Detect the encoding of the file using chardet
    with open(EXCEL_FILE_PATH, 'rb') as file:
        result = chardet.detect(file.read())  # Auto-detect the encoding
        file_encoding = result['encoding']

    # Load the CSV file with the detected encoding
    df = pd.read_csv(EXCEL_FILE_PATH, encoding=file_encoding)

    # Convert to a list of dictionaries for easy iteration in the template
    players = df.to_dict(orient='records')

    # Get the column headers from the DataFrame
    columns = df.columns.tolist()

    # Get query parameters for filtering, sorting, and pagination
    team_filter = request.GET.get('player_Team', '')
    position_filter = request.GET.get('player_Position', '')
    status_filter = request.GET.get('player_Status', '')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'player_Name')
    order = request.GET.get('order', 'asc')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))

    # Apply filters
    if team_filter:
        players = [player for player in players if team_filter.lower() in player.get('player_Team', '').lower()]
    if position_filter:
        players = [player for player in players if position_filter.lower() in player.get('player_Position', '').lower()]
    if status_filter:
        players = [player for player in players if status_filter.lower() in player.get('player_Status', '').lower()]
    if search_query:
        players = [player for player in players if any(search_query.lower() in str(value).lower() for value in player.values())]

    # Apply sorting
    ascending = True if order == 'asc' else False
    if sort_by in columns:
        players = sorted(players, key=lambda x: x.get(sort_by, ''), reverse=not ascending)

    # Pagination
    total_items = len(players)
    start = (page - 1) * per_page
    end = start + per_page
    players_page = players[start:end]
    total_pages = -(-total_items // per_page)  # Ceiling division

    context = {
        'players': players_page,
        'columns': columns,
        'current_page': page,
        'total_pages': total_pages,
        'team_filter': team_filter,
        'position_filter': position_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
    }

    return render(request, 'FPLapp/player_stats.html', context)

def user_register(request):
    form = LoginRegisterForm()
    if request.method == 'POST':
        form = LoginRegisterForm(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            if User.objects.filter(username=un).exists():
                messages.warning(request, 'User already exists, try another username.')
            else:
                new_user = User(username=un)
                new_user.set_password(pw)
                new_user.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('/login/')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the errors in the form.')

    return render(request, 'FPLapp/register.html', {'form': form})

def user_login(request):
    form = LoginRegisterForm()
    if request.method == 'POST':
        form = LoginRegisterForm(request.POST)
        un = request.POST.get('username')
        pw = request.POST.get('password')
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/')  # Redirect to the home page (player_stats)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'FPLapp/login.html', {'form': form})

@login_required(login_url='/login/')
def manage_squad(request, player_id):
    customer = request.user
    player = get_object_or_404(Player, id=player_id)
    squad = Squad.objects.filter(username=customer)
    action = request.GET.get('action')

    if action == 'add_or_replace':
        if squad.filter(player=player).exists():
            messages.info(request, f"{player.player_Name} is already in your squad.")
        elif squad.count() >= 15:
            messages.error(request, "Your squad is already full.")
        else:
            Squad.objects.create(username=customer, player=player)
            messages.success(request, f"{player.player_Name} added to your squad.")

    elif action == 'remove':
        if not squad.filter(player=player).exists():
            messages.error(request, "Player not found in your squad.")
        else:
            squad.filter(player=player).delete()
            messages.success(request, f"{player.player_Name} removed from your squad.")

    return render(request, 'FPLapp/squad.html', {'squad': squad})

@login_required(login_url='/login/')
def save_squad_changes(request):
    customer = request.user
    squad = Squad.objects.filter(username=customer)

    if squad.count() != 15:
        messages.error(request, "You must have exactly 15 players in your squad before saving.")
    else:
        for entry in squad:
            entry.squad_Status = "Saved"
            entry.save()
        messages.success(request, "Squad changes saved successfully.")

    return render(request, 'FPLapp/squad.html', {'squad': squad})

@login_required(login_url='/login/')
def reset_squad_changes(request):
    customer = request.user
    Squad.objects.filter(username=customer).delete()
    messages.success(request, "Squad reset to the previous saved state.")
    return render(request, 'FPLapp/squad.html', {'squad': []})

@login_required(login_url='/login/')
def manage_xi(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    customer = request.user
    xi = XI.objects.filter(username=customer)
    action = request.GET.get('action')

    if action == 'change_role':
        existing_xi = xi.filter(player=player).first()
        if existing_xi:
            # Toggle between Playing and Bench roles
            if existing_xi.player_Role == 'Playing':
                existing_xi.player_Role = 'Bench'
            else:
                existing_xi.player_Role = 'Playing'
            existing_xi.save()
            messages.success(request, f"{player.player_Name} role updated to {existing_xi.player_Role}.")
        else:
            messages.error(request, "Player not found in your XI.")

    elif action == 'set_captain':
        # Check if the player is already in the "Playing" XI
        if xi.filter(player=player, player_Role='Playing').exists():
            # Ensure that only one player is captain
            if xi.filter(captain=True).exists():
                # Remove the current captain status
                xi.filter(captain=True).update(captain=False)

            # Ensure the player is not already vice-captain
            if xi.filter(vice_captain=True, player=player).exists():
                messages.error(request, "A player cannot be both captain and vice-captain.")
                return render(request, 'FPLapp/xi.html', {'xi': xi})

            # Set the new captain
            xi.filter(player=player).update(captain=True)
            messages.success(request, f"{player.player_Name} is now your captain.")
        else:
            messages.error(request, "Player must be in the Playing XI to be set as captain.")

    elif action == 'set_vice_captain':
        # Check if the player is already in the "Playing" XI
        if xi.filter(player=player, player_Role='Playing').exists():
            # Ensure that only one player is vice-captain
            if xi.filter(vice_captain=True).exists():
                # Remove the current vice-captain status
                xi.filter(vice_captain=True).update(vice_captain=False)

            # Ensure the player is not already captain
            if xi.filter(captain=True, player=player).exists():
                messages.error(request, "A player cannot be both captain and vice-captain.")
                return render(request, 'FPLapp/xi.html', {'xi': xi})

            # Set the new vice-captain
            xi.filter(player=player).update(vice_captain=True)
            messages.success(request, f"{player.player_Name} is now your vice-captain.")
        else:
            messages.error(request, "Player must be in the Playing XI to be set as vice-captain.")

    return render(request, 'FPLapp/xi.html', {'xi': xi})

@login_required(login_url='/login/')
def save_xi_changes(request):
    customer = request.user
    xi = XI.objects.filter(username=customer)

    if xi.filter(player_Role='Playing').count() != 11:
        messages.error(request, "You must have exactly 11 players in the playing XI before saving.")
    else:
        xi.update(xi_Status="Saved")
        messages.success(request, "XI changes saved successfully.")

    return render(request, 'FPLapp/xi.html', {'xi': xi})

@login_required(login_url='/login/')
def reset_xi_changes(request):
    customer = request.user
    XI.objects.filter(username=customer).delete()
    messages.success(request, "XI reset to the previous saved state.")
    return render(request, 'FPLapp/xi.html', {'xi': []})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('/login/')

