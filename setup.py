import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EmojiCloud",
    version="0.3.0",
    authors=[
        { "name": "Yunhe Feng", "email":  "yunhe.feng@unt.edu" },
        { "name": "Bowang Lan", "email": "blan2@uw.edu" }
    ],
    description="EmojiCloud: a Tool for Emoji Cloud Visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BowangLan/emoji-cloud-engine",
    project_urls={
        "Bug Tracker": "https://github.com/BowangLan/emoji-cloud-engine/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    include_package_data=True,
    package_data={
        "EmojiCloud": ["data/*/*.png"]
    }
)


