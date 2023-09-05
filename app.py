import streamlit as st


st.header('scrollable text')

### scrollable text ###

text_content = """
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in odio nec turpis ultricies vehicula ac ut orci. Nullam auctor nisi et est semper blandit. Sed in interdum nulla. Vivamus ut facilisis dui. Fusce nec ex purus. Integer vel feugiat odio, at fermentum lectus.</p>
<p>Phasellus fringilla justo eu orci faucibus, id iaculis purus varius. Maecenas a quam vitae urna suscipit egestas. Duis hendrerit, nunc id cursus sollicitudin, quam velit venenatis odio, in elementum ipsum erat vel sapien.</p>
<!-- Add more text here -->
"""

scrollable_element = f"""
    <div class="scroll-container">
        {text_content}
"""


st.markdown(scrollable_element, unsafe_allow_html=True)


### Contact Form ###

st.header(':mailbox: User feedback')


contact_form = """
<form action="https://formsubmit.co/jermwatt@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="your name" required>
     <input type="email" name="email" placeholder="your email" required>
    <textarea name="message" placeholder="Details of your problem"></textarea>
     <button type="submit">Send</button>
</form>
"""

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

st.markdown(contact_form, unsafe_allow_html=True)
