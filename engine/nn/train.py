import torch
from tqdm import tqdm

def train_model(model, train_loader, valid_loader, criterion, optimizer, num_epochs=75, patience=10):
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    best_loss = float('inf')
    patience_counter = 0
    model.to(device)
    
    for epoch in tqdm(range(num_epochs)):
        model.train()
        train_loss = 0.0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        
        model.eval()
        valid_loss = 0.0
        with torch.no_grad():
            for inputs, targets in valid_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                valid_loss += loss.item()
        
        valid_loss /= len(valid_loader)
        
        print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Valid Loss: {valid_loss:.4f}')
        
        if valid_loss < best_loss:
            best_loss = valid_loss
            best_model_wts = model.state_dict().copy()
            patience_counter = 0
        else:
            patience_counter += 1
        
        if patience_counter >= patience:
            print('Early stopping')
            break
    
    model.load_state_dict(best_model_wts)
    return model
