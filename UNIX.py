import torch
from unixcoder import UniXcoder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = UniXcoder("microsoft/unixcoder-base")
model.to(device)
model_weights_path = "C:/Users/ASUS/Desktop/Code/cbert/u1/saved_models5/java/checkpoint-best-bleu/pytorch_model.bin"
# Load the model weights
state_dict = torch.load(model_weights_path, map_location=device)

# Load the weights into the model
model.load_state_dict(state_dict, strict=False)

# Set the model to evaluation mode (important for inference)
model.eval()
context = """
public static void CHeckcondition(int <mask0>) {
        System.out.println("Checking conditions for numbers from 1 to " + <mask0> + ":");

        for (int i = 1; i <= <mask0>; i++) {
            if (i % 2 == 0) {
                System.out.println(i + " is even.");
            } else {
                System.out.println(i + " is odd.");
            }
        }
    }
"""
tokens_ids = model.tokenize([context],max_length=512,mode="<encoder-decoder>")
source_ids = torch.tensor(tokens_ids).to(device)
prediction_ids = model.generate(source_ids, decoder_only=False, beam_size=3, max_length=128)
predictions = model.decode(prediction_ids)
print([x.replace("<mask0>","").strip() for x in predictions[0]])