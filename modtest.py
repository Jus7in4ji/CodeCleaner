import torch
from transformers import RobertaConfig, RobertaTokenizer
from transformers import RobertaModel

from model import Seq2Seq  # Assuming your custom model class is named Seq2Seq

# Define the model directory
output_dir = "C:/Users/ASUS/Desktop/Code/cbert/u1/saved_models3/java/checkpoint-best-bleu"

# Load tokenizer and configuration
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
# Load configuration and adjust for checkpoint parameters
config = RobertaConfig.from_pretrained('roberta-base')
config.is_decoder = True
config.vocab_size = 51416  # Match vocab size in checkpoint
config.max_position_embeddings = 1026  # Match positional embeddings in checkpoint
config.type_vocab_size = 10  # Match token type embeddings in checkpoint


# Initialize the encoder model (RobertaModel) and Seq2Seq model
encoder = RobertaModel.from_pretrained('roberta-base', config=config, ignore_mismatched_sizes=True)
model = Seq2Seq(encoder=encoder, decoder=encoder, config=config, beam_size=10, max_length=32,
                sos_id=tokenizer.convert_tokens_to_ids(["<mask0>"])[0],
                eos_id=tokenizer.sep_token_id)

# Load the saved model weights
model_file = f"{output_dir}/pytorch_model.bin"
model.load_state_dict(torch.load(model_file))

# Move model to the appropriate device (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set the model to evaluation mode before inference
model.eval()

# Example of making predictions
# Assuming you have input data preprocessed into token IDs
input_ids = torch.tensor([tokenizer.encode('sum = a+b;')]).to(device)
with torch.no_grad():
    outputs = model(input_ids)
    # Convert model output IDs to text
    predicted_text = tokenizer.decode(outputs[0][0], skip_special_tokens=True)

print("Predicted text:", predicted_text)
